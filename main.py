import speech_recognition as sr
# It is used to just convert voice to text.
import webbrowser
# it is used to open browser like chrome,youtube etc...
import pyttsx3
# it is used to convert text to voice and it is a computer voice
import music_library
# it is a user defined library which hold some url of songs
import requests
# it is used request server like user say news,python send requast to newsapi and then json is used to read by python
from openai import OpenAI
# it is used to get solution asked by user,just flow like this..python-openai-ChatGpt-answer-python-speaker...this is the workflow of this
from gtts import gTTS
# it is also convert text to voice and it is a google voice
import pygame
# it is a speaker i.e it is basically used to play mp3 saved by gTTs
import os
# it is used to connect operating system

# pip install pocketsphinx

# recognizer = sr.Recognizer()
# engine = pyttsx3.init() 
newsapi = "<Leaving this api right now>"

# def speak_old(text):
#     engine.say(text)
#     engine.runAndWait()
# this is used for speaking but their is looked like robotic so i just change this to google voice

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        if song in music_library.music:
           webbrowser.open(music_library.music[song])
        else:
          webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # JSON response
            data = r.json()
            
            # Extract the article
            articles = data.get('articles', [])
            
            # Print the headline
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request furtheer.....
        output = aiProcess(c)
        speak(output) 





if __name__ == "__main__":
    speak("Initializing Jarvis....")

    r = sr.Recognizer()

    while True:
        print("Recognizing...")

        try:
            # strt Word
            with sr.Microphone(device_index=1) as source:
                print("Adjusting microphone...")
                r.adjust_for_ambient_noise(source, duration=2)

                print("Say: Jarvis")
                audio = r.listen(source, timeout=10, phrase_time_limit=10)

            try:
                word = r.recognize_google(audio)
                print("You said:", word)

            except sr.UnknownValueError:
                print("Speech not recognized.")
                continue

            except sr.RequestError:
                print("Internet connection error.")
                continue

            if "jarvis" in word.lower():
                speak("Yes")

                # Command line
                with sr.Microphone(device_index=1) as source:
                    print("Listening for command...")
                    r.adjust_for_ambient_noise(source, duration=1)

                    audio = r.listen(source, timeout=8, phrase_time_limit=8)

                try:
                    command = r.recognize_google(audio)
                    print("Command:", command)

                    processCommand(command)

                except sr.UnknownValueError:
                    print("Command not recognized.")

                except sr.RequestError:
                    print("Internet connection error.")

        except Exception as e:
            print("Error:", e)