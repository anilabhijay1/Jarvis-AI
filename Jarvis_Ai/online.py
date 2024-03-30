import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)

def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey"
                          f"=470b998a878b45a5a7599db4e7876be4").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article['title'])
    return news_headline[:6]


def weather_forecast(city):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid"
                       f"=cb626a8bc741af43c3588467402148ff").json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather,f"{temp}°C",f"{feels_like}°C"






