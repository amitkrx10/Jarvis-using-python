import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests   

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "4a61ec5dc05d46d48d3ea7fd27e87354"   # my API key of gimini 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.replace("play", "").strip().lower()
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I don't know that song.")
            print("Song not found:", song)

    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-08-14&sortBy=publishedAt&apiKey=4a61ec5dc05d46d48d3ea7fd27e87354")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if articles:
                    speak("Here are the top headlines.")
                    for article in articles[:5]:   
                        speak(article['title'])
                else:
                    speak("Sorry, I could not find any news right now.")
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            print("News Error:", e)
            speak("There was an error while fetching the news.")


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}")

            if "jarvis" in word.lower():
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis activated...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print(f"Command: {command}")
                processCommand(command)

        except Exception as e:
            print("Error:", e)
