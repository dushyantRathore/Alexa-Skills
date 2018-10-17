from flask import Flask
from flask_ask import Ask, statement, question
from bs4 import BeautifulSoup
import requests
import re


app = Flask(__name__)
ask = Ask(app, "/live_scores")


def get_scores():
    url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
    score_file = requests.post(url)
    score_html = score_file.text
    score_file.close()

    soup = BeautifulSoup(score_html, 'html.parser')

    a = soup.find_all('div', attrs={'class': 'innings-info-1'})
    b = soup.find_all('div', attrs={'class': 'innings-info-2'})
    c = soup.find_all('div', attrs={'class': 'match-status'})

    teamA = []
    teamB = []
    status = []

    for results in a:
        t_a = results.text
        t_a = t_a.replace("ov", " overs ")
        t_a = t_a.replace("/", " for ")
        teamA.append(t_a)

    for results in b:
        t_b = results.text
        t_b = t_b.replace("ov", " overs ")
        t_b = t_b.replace("/", " for ")
        teamB.append(t_b)

    for results in c:
        s = results.text
        s = re.sub("[\(\[].*?[\)\]]", "", s)
        status.append(s)

    # Strip Characters
    teamA = list(map(lambda s: s.strip(), teamA))
    teamB = list(map(lambda s: s.strip(), teamB))
    status = list(map(lambda s: s.strip(), status))

    return teamA,teamB,status


@ask.launch  # On launching the skill
def start_skill():
    message = "Hello, would you like to get the live cricket scores ?"
    return question(message)  # As a form of a question


@ask.intent("YesIntent")
def share_score():
    message = "The live scores are . "
    teamA,teamB,status = get_scores()

    for i in range(0,len(teamA)):
        message += "Match Number " + str(i+1) + " . " + "Status . " + str(status[i]) + " . "
        message += "Team A . " + str(teamA[i]) + " . "
        message += "Team B . " + str(teamB[i]) + " . "

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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
    # a,b,c = get_scores()
    # print a
    # print b
    # print c


