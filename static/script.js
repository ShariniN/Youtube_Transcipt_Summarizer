async function processVideo() {
    const url = document.getElementById('url').value;
    const question = document.getElementById('question').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/process_video', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, question: question }), 
        });

        if (!response.ok) {
            const errorText = await response.text(); 
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        document.getElementById('summary').innerText = data.summary || "No summary available.";
        document.getElementById('answer').innerText = data.answer || "No answer available.";

    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to process the video. Please check the console for details.");
    }
}