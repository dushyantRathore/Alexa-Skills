from flask import Flask
from flask_ask import Ask, statement, question
import urllib2
from bs4 import BeautifulSoup
import requests
import re


app = Flask(__name__)
ask = Ask(app, "/live_scores")


def get_scores():
    url = "http://www.espncricinfo.com/scores/"
    score_file = urllib2.urlopen(url)
    score_html = score_file.read()
    score_file.close()

    soup = BeautifulSoup(score_html, 'html.parser')

    teamA = []
    teamB = []

    scoreA = []
    scoreB = []

    for ul in soup.find_all('li', attrs={'class': 'cscore_item cscore_item--home'}):
        for span in ul.find_all("span", attrs={"class": "cscore_name cscore_name--long"}):
            teamA.append(str(span.text))
        for div in ul.find_all("div", attrs={"class": "cscore_score"}):
            score = str(div.text)
            score = score.replace("(", "")
            score = score.replace(")", "")
            score = score.replace("/", " for ")
            score = score.replace("ov", "overs")
            scoreA.append(score)

    for ul in soup.find_all('li', attrs={'class': 'cscore_item cscore_item--away'}):
        for span in ul.find_all("span", attrs={"class": "cscore_name cscore_name--long"}):
            teamB.append(str(span.text))
        for div in ul.find_all("div", attrs={"class": "cscore_score"}):
            score = str(div.text)
            score = score.replace("(", "")
            score = score.replace(")", "")
            score = score.replace("/", " for ")
            score = score.replace("ov", "overs")
            scoreB.append(score)

    # Strip Characters
    teamA = map(lambda s: s.strip(), teamA)
    teamB = map(lambda s: s.strip(), teamB)
    scoreA = map(lambda s: s.strip(), scoreA)
    scoreB = map(lambda s: s.strip(), scoreB)

    return teamA,teamB,scoreA,scoreB


@ask.launch  # On launching the skill
def start_skill():
    message = "Hello, would you like to get the live cricket scores ?"
    return question(message)  # As a form of a question


@ask.intent("YesIntent")
def share_score():
    message = "Sorry, still working on it."
    
    teamA,teamB,scoreA,scoreB = get_scores()

    print teamA, teamB, scoreA, scoreB

    for i in range(0,len(teamA)):
        message += "Match Number " + str(i+1) + " . "
        message += "Team A . " + str(teamA[i]) + " . "
        message += "Team B . " + str(teamB[i]) + " . "
        message += "Score of Team A . " + str(scoreA[i]) + " . "
        message += "Score of Team B . " + str(scoreB[i]) + " . "

    return statement(message)


@ask.intent("NoIntent")
def no_intent():
    message = "Sure, no problem. It was nice talking to you"
    return statement(message)


@ask.intent("AMAZON.HelpIntent")
def help():
    message = "This skill gives details about the live cricket matches from all around the world. Reply with a yes " \
              "to get the live scores or with a no to exit the skill after invocation. Would you like to start ?"
    return question(message)


@ask.intent("AMAZON.StopIntent")
def stop():
    message = "Thank you for using live cricket scores . "
    return statement(message)


@ask.intent("AMAZON.CancelIntent")
def cancel():
    message = "Thank you for using live cricket scores . "
    return statement(message)


@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World"

@app.route("/live", methods=["GET", "POST"])
def live():
    message = "The live scores are . "
    
    teamA,teamB,scoreA,scoreB = get_scores()

    print teamA, teamB, scoreA, scoreB

    for i in range(0,len(teamA)):
        message += "Match Number " + str(i+1) + " . "
        message += "Team A . " + str(teamA[i]) + " . "
        message += "Team B . " + str(teamB[i]) + " . "
        message += "Score of Team A . " + str(scoreA[i]) + " . "
        message += "Score of Team B . " + str(scoreB[i]) + " . "

    return message

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')