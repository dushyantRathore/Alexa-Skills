from flask import Flask
from flask_ask import Ask, statement, question
from bs4 import BeautifulSoup
import requests
import re
import json

app = Flask(__name__)
ask = Ask(app, "/weather_fetcher")


@ask.launch  # On launching the skill
def start_skill():
    message = "Hello, would you like to get the live weather conditions of a city?"
    return question(message)  # As a form of a question - to leave the session open


@ask.intent("YesIntent")
def yes_intent():
    message = "Please provide the city for which you want to get the weather details. "
    return question(message)  # As a form of question to leave the session open


@ask.intent("NoIntent")
def no_intent():
    message = "Sure, no problem. It was nice talking to you."
    return statement(message)   # Close the session


@ask.intent("weatherintent", convert={'place': str})
def get_weather(place):
    print(place)
    weather_api_key = "a4c44b228e720ea728b757f3aa754c06"
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params={'q': place, 'APPID': weather_api_key,
                    'units': 'metric'})
    print(r)
    r = json.loads(r.text)
    description = str(r["weather"][0]["description"])
    current_temp = str(r["main"]["temp"])
    max_temp = str(r["main"]["temp_max"])
    min_temp = str(r["main"]["temp_min"])
    humidity = str(r["main"]["humidity"])

    response_message = ""
    response_message = response_message + "\nPlace : " + place + " . "
    response_message = response_message + "\nDescription : " + description + " . " 
    response_message = response_message + "\nCurrent Temperature : " + current_temp + " degrees celcius . "
    response_message = response_message + "\nMaximum Temperature : " + max_temp + " degrees celcius . "
    response_message = response_message + "\nMinimum Temperature : " + min_temp + " degrees celcius . "
    response_message = response_message + "\nHumidity : " + humidity + " percent . "

    print(response_message)
    return statement(response_message)


@ask.intent("AMAZON.HelpIntent")
def help():
    message = "This skill fetches the current weather of the location provided by the user. Would you like to start ?"
    return question(message)


@ask.intent("AMAZON.StopIntent")
def stop():
    message = "Thank you for using weather fetcher."
    return statement(message)

@ask.intent("AMAZON.CancelIntent")
def cancel():
    message = "Thank you for using weather fetcher."
    return statement(message)

@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
