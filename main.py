import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai
from ddgs import DDGS
from dotenv import load_dotenv
import os
import logging
import fitz
from tkinter import Tk, filedialog
import re

# Loads the .env file
load_dotenv()


# ---------------- GEMINI API CONFIG ----------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# -------------- SPEAK FUNCTION ----------------
def speak(text):
    try:
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Male voice
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[Speak Error]: {e}")

# -------------- TEXT CLEANING FOR SPEECH ----------------
def clean_text_for_speech(text):
    # Remove common markdown symbols and formatting
    text = re.sub(r"[*_`#>\[\]\(\)\{\}\\\/]", "", text)       
    text = re.sub(r"\$.*?\$", "", text)             
    text = re.sub(r"[|~^=<>\+]", "", text)    
    text = re.sub(r"\n+", ". ", text)                 
    text = re.sub(r"\.{2,}", ".", text)        
    text = re.sub(r"\s+", " ", text)       
    return text.strip()



# -------------- AI PROCESSING ----------------
def aiProcess(command):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(command)
        cleaned = clean_text_for_speech(response.text)
        speak(cleaned)
    except Exception as e:
        speak("Something went wrong with the AI response.")
        logging.error(f"[Gemini Error]: {e}") 

# -------------- IMAGE SEARCHING ----------------
def fetch_and_show_image(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.images(query)
            image_url = results[0]['image'] 
            speak("Here is what I found.")
            webbrowser.open(image_url)
    except Exception as e:
        speak("Sorry, I couldn't find an image.")
        print(f"[Image Error]: {e}")

# -------------- WEATHER SEARCHING ----------------
def get_weather(city):
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            speak(f"Sorry, I couldn't find the weather for {city}.")
            return

        temp = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        report = (
            f"The temperature in {city} is {temp}°C with {description}. "
            f"Humidity is {humidity}% and wind speed is {wind} meters per second."
        )
        speak(report)

    except Exception as e:
        speak("There was a problem fetching the weather.")
        logging.error(f"[Weather Error]: {e}")


# -------------- PDF SUMMARIZER  ----------------
def summarize_pdf_with_picker():
    try:
        # Hide root tkinter window
        root = Tk()
        root.withdraw()

        # Open file picker dialog
        speak("Please choose a file to summarize from the dialog.")
        file_path = filedialog.askopenfilename(
            title="Select PDF to Summarize",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not file_path:
            speak("No file selected.")
            return

        # Read PDF content
        with fitz.open(file_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()

        if not text.strip():
            speak("Sorry, the PDF seems to be empty.")
            return

        speak("Summarizing the document, please wait.")
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(f"Summarize this document:\n\n{text[:6000]}")
        cleaned = clean_text_for_speech(response.text)
        speak(cleaned)

    except Exception as e:
        speak("Failed to summarize the PDF.")
        logging.error(f"[PDF Summary Error]: {e}")


# -------------- COMMAND HANDLER ----------------
def processCommand(command):
    command = command.lower()
    print(f"You Said: {command}")

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")


# -------------- MUSIC HANDLER ----------------
    elif command.startswith("play"):
        try:
            song = " ".join(command.split(" ")[1:]).strip().lower()
            if song in musicLibrary.music:
                speak(f"Playing {song}")
                webbrowser.open(musicLibrary.music[song])
            else:
                speak(f"Sorry, I couldn't find the song {song} in your music library.")
        except Exception as e:
            speak("Something went wrong while trying to play the music.")
            print(f"[Music Error]: {e}")


# -------------- NEWS HANDLER ----------------
    elif "news" in command:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={os.getenv('NEWS_API_KEY')}")
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                for article in articles[:5]:  # Limit to top 5 headlines
                    speak(article['title'])
        except Exception as e:
            speak("Sorry, I couldn't fetch the news.")
            print(f"[News Error]: {e}")


# -------------- EXIT HANDLER ----------------
    elif "stop" in command or "exit" in command:
        speak("Goodbye sir, have a nice day!")
        exit()

# -------------- IMAGE HANDLER ----------------
    elif "image" in command or "picture" in command or "show me" in command:
        try:
            search_query = command.replace("show me", "").replace("a picture of", "").replace("image", "").strip()
            speak(f"Searching for an image of {search_query}")
            fetch_and_show_image(search_query)
        except Exception as e:
            speak("There was an issue finding the image.")
            print(f"[Image Search Error]: {e}")


# -------------- WEATHER HANDLER ----------------
    elif "weather" in command:
        try:
            words = command.split()
            for i in range(len(words)):
                if words[i] == "in" and i + 1 < len(words):
                    city = " ".join(words[i+1:])
                    get_weather(city)
                    return
            speak("Please specify the city name, like 'weather in Delhi'.")
        except Exception as e:
            speak("Couldn't understand the city.")
            logging.error(f"[WeatherCommand Error]: {e}")


# -------------- PDF HANDLER ----------------
    elif "summarise" in command or "pdf" in command:
        try:
            summarize_pdf_with_picker()
        except Exception as e:
            speak("Something went wrong while summarizing the PDF.")
            logging.error(f"[PDF Command Error]: {e}")


# -------------- AI COMMAND HANDLER ----------------
    # -------------- AI COMMAND HANDLER ----------------
    else:
        response = aiProcess(command)
        speak(response)
        return command, response  # <-- Add this



# -------------- MAIN LOOP ----------------
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                wake_word = recognizer.recognize_google(audio).lower()

            if "jarvis" in wake_word:
                speak("Yes sir")
                with sr.Microphone() as source:
                    print("Listening...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        except sr.UnknownValueError:
            print("[Info]: Didn't catch that.")
        except sr.RequestError:
            print("[Error]: Could not reach the speech API.")
        except Exception as e:
            print(f"[Unhandled Exception]: {e}")
