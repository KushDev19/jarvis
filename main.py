import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
from openai import OpenAI
import pygame
import asyncio
import edge_tts

recognizer = sr.Recognizer()

newsapi = "8321475cbaa64061b7c58a7fe77607cf"
    
async def tts_play(text, voice="en-US-AriaNeural", rate="+20%"):
    # Create the TTS stream
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    # Save to file
    await communicate.save("jarvis.mp3")

    # Play with pygame
    pygame.mixer.init()
    pygame.mixer.music.load("jarvis.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

# wrapper to call from sync code
def speak(text, voice="en-US-AriaNeural", rate="+20%"):
    asyncio.run(tts_play(text, voice, rate))

    
def aiProcess(command):
    client = OpenAI(
    api_key="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"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general task like alexa and google cloud and try to give short and precise responses."},
            {"role": "user", "content" : command}
        ]
    )
    print(completion.choices[0].message.content)
    speak(completion.choices[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open('https://google.com')
        speak("yeah")
    elif "open youtube" in c.lower():
        webbrowser.open('https://youtube.com')
        speak("yeah")
    elif "open facebook" in c.lower():
        webbrowser.open('https://facebook.com')
        speak("yeah")
    elif "open spotify" in c.lower():
        webbrowser.open('https://spotify.com')
        speak("yeah")
    elif "open instagram" in c.lower():
        webbrowser.open('https://instagram.com')
        speak("yeah")
    elif "open youtube music" in c.lower():
        webbrowser.open('https://music.youtube.com')
        speak("yeah")
    elif c.lower().startswith("play"):
        song = (c.lower().strip())[5:]
        link = musicLibrary.music[song]
        webbrowser.open(link)
        speak("yeah")
    elif "news" in c.lower():
        speak("Here is the News")
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=8321475cbaa64061b7c58a7fe77607cf")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("News Fetch Failed!")
    else:
        #let openAI handle the request
        aiProcess(c)
    

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            print(word)
            if("jarvis" in word.lower()):
                speak("aahah?...")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(command)
                    
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
        
        