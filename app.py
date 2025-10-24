from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
from pytube import YouTube
import whisper
import os
import re
import logging
import nltk

nltk.download('punkt')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# Load Whisper model
try:
    logger.info("Loading Whisper model...")
    whisper_model = whisper.load_model("small")  
    logger.info("Whisper model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading Whisper model: {e}")
    whisper_model = None

try:
    logger.info("Loading LongT5 model...")
    longt5_tokenizer = T5Tokenizer.from_pretrained("google/long-t5-tglobal-base")
    longt5_model = T5ForConditionalGeneration.from_pretrained("google/long-t5-tglobal-base")
    logger.info("LongT5 model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading LongT5 model: {e}")
    longt5_model = None

@app.route('/process_video', methods=['POST'])
def process_video():
    logger.info("Processing video...")
    data = request.json
    url = data.get('url')
    question = data.get('question', None)

    if not url:
        logger.error("No URL provided.")
        return jsonify({"error": "URL is required"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        logger.error(f"Invalid YouTube URL: {url}")
        return jsonify({"error": "Invalid YouTube URL"}), 400

    logger.info(f"Extracted video ID: {video_id}")
    transcript = get_transcript(video_id) or transcribe_audio(download_audio(video_id))

    if not transcript:
        logger.error("Unable to fetch or generate transcript.")
        return jsonify({"error": "Unable to fetch or generate transcript"}), 400

    # Clean transcript before processing
    cleaned_transcript = clean_text(transcript)

    # Generate a detailed summary using LongT5
    summary = summarize_with_longt5(cleaned_transcript)
    if not summary:
        logger.error("Unable to summarize transcript.")
        return jsonify({"error": "Unable to summarize transcript"}), 400

    response = {"summary": summary}

    # Answer the question if provided
    if question:
        logger.info(f"Answering question: {question}")
        response["answer"] = answer_question(cleaned_transcript, question) or "Unable to answer the question."
    
    logger.info("Video processed successfully.")
    return jsonify(response)

# Extract video ID from YouTube URL
def extract_video_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.*\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Fetch transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        logger.error(f"Transcript error: {e}")
        return None

# Download YouTube audio
def download_audio(video_id):
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            file_path = audio_stream.download(output_path="./", filename=f"{video_id}.mp4")
            return file_path
        return None
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return None


def transcribe_audio(file_path):
    if not whisper_model or not file_path:
        return None
    try:
        transcript = whisper_model.transcribe(file_path)["text"]
        os.remove(file_path)  
        return transcript
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return None

# Clean text to improve processing
def clean_text(text):
    if not text:
        return ""
    
    # Remove speaker labels (e.g., "Stephen:", "Guest:")
    text = re.sub(r'^\w+:\s*', '', text, flags=re.MULTILINE)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters except basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\.,!?\'" ]', '', text)
    # Remove multiple periods or other punctuation
    text = re.sub(r'\.{2,}', '.', text)
    text = text.strip()
    
    logger.info("Text cleaned successfully.")
    return text

# Summarize with LongT5
def summarize_with_longt5(text, max_input_length=4096, max_summary_length=500):
    if not longt5_model:
        return "Summarization model not available."

    try:
        # Tokenize the input text
        inputs = longt5_tokenizer("summarize: " + text, return_tensors="pt", max_length=max_input_length, truncation=True)
        # Generate the summary
        summary_ids = longt5_model.generate(inputs["input_ids"], max_length=max_summary_length)
        # Decode the summary
        summary = longt5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        logger.error(f"Error summarizing with LongT5: {e}")
        return None

# Answer questions using QA pipeline
def answer_question(transcript, question):
    try:
        qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
        return qa_pipeline(question=question, context=transcript)['answer']
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)
