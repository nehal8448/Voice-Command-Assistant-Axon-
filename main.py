import speech_recognition as sr
import webbrowser
import pyttsx3
import pywhatkit
from googlesearch import search
import json
import os
from openai import OpenAI

engine = pyttsx3.init()

# Load memory
memory_file = "memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {"user_name": "Nehal", "last_topic": None}

def save_memory():
    with open(memory_file, "w") as f:
        json.dump(memory, f)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def smart_open(site_name):
    try:
        for url in search(site_name, num_results=1):
            speak(f"Opening {site_name}")
            webbrowser.open(url)
            memory["last_topic"] = site_name
            save_memory()
            return
        speak("Sorry, I couldn't find that site.")
    except Exception as e:
        speak("Something went wrong while searching.")
        print(e)
#updated 1
def smart_open(site_name):
    try:
        # Special case for Spotify app
        if "spotify" in site_name.lower():
            spotify_path = r"https://open.spotify.com/"  
            if os.path.exists(spotify_path):
                speak("Opening Spotify app")
                os.startfile(spotify_path)
                memory["last_topic"] = "Spotify"
                save_memory()
                return
            else:
                speak("Spotify app not found, opening Spotify website instead.")
                webbrowser.open("https://open.spotify.com")
                memory["last_topic"] = "Spotify"
                save_memory()
                return
        # Default: open first Google search result
        for url in search(site_name, num_results=1):
            speak(f"Opening {site_name}")
            webbrowser.open(url)
            memory["last_topic"] = site_name
            save_memory()
            return
        speak("Sorry, I couldn't find that site.")
    except Exception as e:
        speak("Something went wrong while searching.")
        print(e)


def detect_intent(command):
    command = command.lower()

    search_phrases = ["can you search for", "can you search", "look up", "tell me about", "search for", "find", "search", "what is", "who is"]
    search_phrases.sort(key=len, reverse=True)
    for phrase in search_phrases:
        if phrase in command:
            return "search", command.replace(phrase, "").strip()

    open_phrases = ["go to", "launch", "open"]
    open_phrases.sort(key=len, reverse=True)
    for phrase in open_phrases:
        if phrase in command:
            return "open", command.replace(phrase, "").strip()

    play_phrases = ["put on", "play"]
    play_phrases.sort(key=len, reverse=True)
    for phrase in play_phrases:
        if phrase in command:
            return "play", command.replace(phrase, "").strip()

    if "my name is" in command:
        name = command.split("my name is")[-1].strip()
        memory["user_name"] = name
        save_memory()
        return "greet_update", name

    return "unknown", command

def processCommand(c):
    intent, content = detect_intent(c)

    if intent == "open":
        smart_open(content)

    elif intent == "play":
        speak(f"Playing {content} on YouTube")
        pywhatkit.playonyt(content)
        memory["last_topic"] = content
        save_memory()

    elif intent == "search":
        speak(f"Searching for {content}")
        webbrowser.open(f"https://www.google.com/search?q={content}")
        memory["last_topic"] = content
        save_memory()

    elif intent == "greet_update":
        speak(f"Nice to meet you, {content}")

    else:
        speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    speak(f"Hello {memory['user_name']}, I am bixby. How can I help you today?")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("listening.....")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if(word.lower() == "bixby"):
                speak("Yes?")
                with sr.Microphone() as source:
                    print("give me command")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("IBM error; {0}".format(e))
