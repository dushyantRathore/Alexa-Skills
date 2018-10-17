from flask import Flask
from flask_ask import Ask, statement, question
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
ask = Ask(app, "/quote_gen")


def quote():
    r = requests.get("https://www.brainyquote.com/quote_of_the_day")
    r = r.text

    soup = BeautifulSoup(r, 'html.parser')

    d = soup.find("div", attrs={"class" : "qotd-q-cntr"})
    quote_text = d.find("a", attrs={"title" : "view quote"}).text
    quote_author = d.find("a", attrs={"title" : "view author"}).text
    result = ""
    result += quote_text + " by "
    result += quote_author

    print(result)
    return result


@ask.launch  # On launching the skill
def start_skill():
    message = "Hello, would you like to get the quote of the day ?"
    return question(message)  # As a form of a question - to leave the session open


@ask.intent("YesIntent")
def yes_intent():
    message = quote()
    return statement(message)  # As a form of a statement


@ask.intent("NoIntent")
def no_intent():
    message = "Sure, no problem. It was nice talking to you."
    return statement(message)   # Close the session


@ask.intent("AMAZON.HelpIntent")
def help():
    message = "This skill fetches the quote of the day for the user. Would you like to hear it?"
    return question(message)


@ask.intent("AMAZON.StopIntent")
def stop():
    message = "Thank you for using quote generator."
    return statement(message)


@ask.intent("AMAZON.CancelIntent")
def cancel():
    message = "Thank you for using quote generator."
    return statement(message)


@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
