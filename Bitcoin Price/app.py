from flask import Flask
from flask_ask import Ask, statement, question
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
ask = Ask(app, "/crypto")


def get_price():
    bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    print(response_json)
    price = str(response_json[0]["price_usd"])
    return price


@ask.launch  # On launching the skill
def start_skill():
    message = "Hello, would you like to know the price of Bitcoin ? "
    return question(message)  # As a form of a question - to leave the session open


@ask.intent("YesIntent")
def yes_intent():
    message = float(get_price())
    message = round(message,2)
    message = "The current price of Bitcoin is : " + str(message) + "dollars."
    return statement(message)  # As a form of statement


@ask.intent("NoIntent")
def no_intent():
    message = "Sure, no problem. It was nice talking to you."
    return statement(message)   # Close the session


@ask.intent("AMAZON.HelpIntent")
def help():
    message = "This skill fetches the current price of Bitcoin for the user. Would you like to know the price ?"
    return question(message)


@ask.intent("AMAZON.StopIntent")
def stop():
    message = "Thank you for using bitcoin price."
    return statement(message)


@ask.intent("AMAZON.CancelIntent")
def cancel():
    message = "Thank you for using bitcoin price."
    return statement(message)


@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
