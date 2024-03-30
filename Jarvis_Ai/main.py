import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you? {USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print("started listening")


def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry, I didn't understand. Can you please repeat that?")
        queri = 'None'
    return queri


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = takeCommand().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you?")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f"Your IP address is {ip_address}"
                )
                print(f"Your IP address is {ip_address}")

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = takeCommand().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = takeCommand().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("What do you want to search on wikipedia sir?")
                search = takeCommand().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)

            elif "give me news" in query:
                speak(f"I am reading out the latest headlines of today,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(),sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report of your city {city}")
                weather,temp,feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp},but it feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("Iam printing weather info on screen")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("please tell me the movie name:")
                text = takeCommand()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline','plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                          f"The plot summary of movie is {plot}")

                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")


            elif "calculate" in query:
                app_id = "8Q9GXJ-J6E3VUUVLH"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I could not find that . Please try again")

            elif "what is" in query or 'who is' in query or 'which is' in query:
                app_id = "8Q9GXJ-J6E3VUUVLH"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        res = client.query(" ".join(text))
                        ans = next(res.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I could not find that")

                except StopIteration:
                    speak("I could not find. Please try again")
