# 🎥 YouTube Transcript Summarizer

An intelligent Flask-based web application that extracts, processes, and summarizes YouTube video content using advanced NLP models. The tool leverages AI to generate concise summaries and answer specific questions about video content without watching the entire video.

---

## 📋 Overview

This application helps users quickly understand YouTube video content by:
- Extracting transcripts from YouTube videos (captions or audio transcription)
- Generating comprehensive summaries using Google's LongT5 model
- Answering specific questions about video content using RoBERTa-based QA
- Supporting videos without captions through Whisper audio transcription

Perfect for students, researchers, content creators, and anyone who needs to quickly digest video information.

---

## ✨ Key Features

### 🎯 Transcript Extraction
- **Automatic Caption Retrieval:** Fetches official YouTube captions when available
- **Audio Transcription Fallback:** Uses OpenAI's Whisper model for videos without captions
- **Multi-format Support:** Handles various YouTube URL formats (youtube.com, youtu.be)

### 📝 AI-Powered Summarization
- **LongT5 Model Integration:** Utilizes Google's Long-T5-TGlobal-Base for handling long-form content
- **Intelligent Text Cleaning:** Removes speaker labels, extra spaces, and irrelevant characters
- **Customizable Length:** Configurable summary length (default: 500 tokens)
- **Context-Aware Processing:** Maintains semantic meaning while condensing content

### 💬 Question Answering
- **Context-Based QA:** Answer specific questions about video content
- **RoBERTa SQuAD2 Model:** State-of-the-art question-answering capabilities
- **Accurate Responses:** Extracts precise answers from transcripts

### 🛠️ Technical Capabilities
- **Robust Error Handling:** Graceful fallbacks for missing transcripts or processing errors
- **Logging System:** Comprehensive logging for debugging and monitoring
- **CORS Support:** Enable cross-origin requests for frontend integration
- **RESTful API:** Clean JSON-based API endpoints

---

## 🧰 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | Flask | Web server and API routing |
| **NLP Models** | Transformers (Hugging Face) | AI model pipeline |
| **Summarization** | LongT5-TGlobal-Base | Long-form text summarization |
| **Q&A System** | RoBERTa-Base-SQuAD2 | Question answering |
| **Audio Transcription** | Whisper (Small) | Speech-to-text conversion |
| **Transcript API** | youtube-transcript-api | YouTube caption extraction |
| **Audio Download** | PyTube | YouTube audio stream download |
| **Text Processing** | NLTK, Regex | Text cleaning and tokenization |
| **Cross-Origin** | Flask-CORS | API accessibility |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB+ RAM (for ML models)


1. **Clone the repository**
```bash
