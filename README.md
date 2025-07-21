# 🤖 Jarvis - AI Voice Assistant (Python Project)

Jarvis is your personal offline-first AI voice assistant, built with Python and powered by **Google Gemini**, **OpenWeather**, and **NewsAPI**. This assistant can speak, listen, search, summarize PDFs, play music, and much more — all through voice control and a wake-word mechanism (“Jarvis”).
This project shows practical integration of speech recognition, APIs, and language models in a modular, real-world system.

---

## 🌟 Project Highlights

- 🎤 **Voice-Controlled:** Wake-word ("Jarvis") activation using microphone input.
- 🤖 **AI Chatbot (Gemini 2.5):** Handles open-ended queries and speaks intelligent answers.
- 🌤️ **Weather Reports:** Real-time weather using OpenWeatherMap API.
- 📄 **PDF Summarization:** Summarizes uploaded PDFs with Gemini and reads them aloud.
- 🖼️ **Image Search:** Searches the web for images and opens results using DuckDuckGo.
- 🎵 **Custom Music Player:** Plays songs from your own YouTube music library.
- 📰 **Live News Headlines:** Fetches breaking news headlines (top 5) via NewsAPI.
- 🔐 **API keys managed via `.env`** for security.

---

## 📁 File Structure
### 📁 Jarvis/
    ├── main.py # Core assistant logic (commands, speech, API handling)
    ├── client.py # Main loop with wake-word detection and voice handling
    ├── musicLibrary.py # Your custom music links stored in a Python dictionary
    ├── .env # API keys (NOT included)
    ├── requirements.txt # Python dependencies
    └── README.md # This documentation
    
---

## 🛠 Installation

1. **Clone the repository**

```bash
git clone https://github.com/sakshamsharma-code/Jarvis-AI-Voice-Assistant.git
cd Jarvis-AI
```

2. **Create a virtual environment**
   
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3.**Install all required modules**

```bash
pip install -r requirements.txt
```
4. Create .env file

In the root directory, add a .env file with your API keys:
```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
NEWS_API_KEY=your_newsapi_api_key_here
```

---

## ▶️ Run the Assistant
```bash
python main.py
You’ll hear:
```
"Initializing Jarvis..."
Then Jarvis listens for the wake-word "Jarvis" to begin command input.

---

🎵 Music Customization
You can customize musicLibrary.py like this:

```python
music = {
    "lofi": "https://www.youtube.com/watch?v=xyz123",
    "motivation": "https://www.youtube.com/watch?v=abc456",
}
```
Then just say:

"Play lofi"
and Jarvis will open the corresponding YouTube link.

---

## 🔐 Environment Variables (.env)
Use this format in your .env file:
```env
GEMINI_API_KEY=your_google_gemini_api_key
WEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
```

---

## 🤝 Credits
Google Gemini API

OpenWeatherMap

NewsAPI.org

DuckDuckGo Search

Built using: SpeechRecognition, pyttsx3, requests, PyMuPDF, webbrowser, google.generativeai,ddgs,dotenv

---

## Author
Developed by Saksham Sharma
