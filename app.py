from os import urandom, environ
from sys import argv

from flask import Flask, render_template, make_response, request, url_for, redirect, abort
import flask_login

from waitress import serve

from google.oauth2 import id_token
from google.auth.transport import requests

from Classes.Block import *
from Classes.User import User, getUser, getGUser, addUser, loadUsers, saveUsers

import ScoutingWorker

# static vars

# app and login
web = Flask(__name__)
web.secret_key = urandom(16)
print('SECRET KEY:' + str(web.secret_key))

googleID = environ.get("GCID")  # THIS SHOULD BE AN ENVIORMENT VARIBLE
googleID += '.apps.googleusercontent.com'

if googleID == None:
    raise Exception("No google ID provided.")

loginManager = flask_login.LoginManager()
loginManager.init_app(web)


@loginManager.user_loader
def loadUser(id):
    return getUser(id)


@web.route('/')
@web.route('/home')
def home():
    return render_template('home.html')


@web.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        try:
            if request.headers['Login-Type'] == "google-signin":
                return googleLogin()
        except KeyError:
            pass
        return login()

    elif request.headers.get("Login-Type") == "LOGOUT":
        flask_login.logout_user()
        return redirect(url_for('home'))

    elif flask_login.current_user.is_authenticated:
        return redirect(url_for('home'))

    return render_template("login.html", retry=False, googleID=googleID)


def googleLogin():
    json = request.get_json()

    # this is ripped directly from google lol
    idinfo = id_token.verify_oauth2_token(
        json['ID'], requests.Request(), googleID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        # not a valid issuer, murder them
        return render_template("login.html", retry=True, googleID=googleID)

    id_ = idinfo['sub']

    user = getGUser(id_)

    if user == None:
        user = User(json['name'], json['email'], id_)

    addUser(user)

    flask_login.login_user(user)

    saveUsers()

    return redirect(url_for('home'))


def login():

    usr = request.form.get('usr')
    psw = request.form.get('psw')

    # TODO: not this...anything but this
    # this login is the equivalent of not having one at all
    # SO because this would be massive security thingy we're just gonna disable this for now :)
    '''if usr == "gulk" and psw == "geist":
        resp = redirect(url_for('home'))
        resp.set_cookie('loggedIn', "true")
        resp.set_cookie('usr', usr)
        return resp

    else:
        return render_template('login.html', retry=True, googleID=googleID)'''
    return render_template('login.html', retry=True, googleID=googleID)


@web.route('/profile/')
@flask_login.login_required
def profilePage():
    return render_template('profile.html', googleID=googleID)


@web.route('/scouting/')
@flask_login.login_required
def matchScoutingPage():
    '''return render_template('matchScouting.html', template=[HeaderBlock("This is an example of a header"), StringBlock('str01', 'This is an example of a string input', 'Sample Text'),
                                                           IntBlock(
                                                               'int01', 'This is an example of a int input', default=1234, max=9999), SpaceBlock(50),
                                                           TallyIntBlock(
        'tally01', 'Above is a space, this is an example of a tally interger box', default=13),
        CheckBoxBlock('chck01', 'This is an example of a check box'), RadioButtonBlock('rdo01', "This is an example of a radio button input", 'Choice1', "Choice2", "Choice3")])'''
    # RIP "bottom text"

    # not too sure why but vscode loves to eat my formatting so thats fun
    template = [HeaderBlock("Robot info"), IntBlock('robot', "Robot #", default=254), IntBlock('match', "Match number"), HeaderBlock("Standstorm"), RadioButtonBlock('startingSide', 'What platform did the robot start on?', '3', '2', '1'), TallyIntBlock('autoPanels', 'How many hatch panels did the robot place? (Auto)'), TallyIntBlock("autoCargo", "How much cargo did the robot place? (Auto)"), TallyIntBlock("autoRocketPanels", "How many panels did the robot put in the rocket? (Auto)"), TallyIntBlock("autoRocketCargo", "How much cargo did the robot put in the rocket? (Auto)"), SpaceBlock(40), HeaderBlock("Teleop"), TallyIntBlock("teleopPanels", "How many hatch panels did the robot place?"), TallyIntBlock("teleopCargo", "How much cargo did the robot place?"), TallyIntBlock("teleopRocketPanels", "How many panels did the robot put in the rocket?"), TallyIntBlock("teleopRocketCargo", "How much cargo did the robot put in the rocket?"), TallyIntBlock("droppedPanels", "How many panels did the robot drop?"), TallyIntBlock(
        "droppedCargo", "How much cargo did the robot drop?"), CheckBoxBlock("playedDefense", "Robot played defense"), CheckBoxBlock("attemptedClimb", "Robot attempted to climb"), CheckBoxBlock("helpedClimb", "Robot helped another robot climb"), CheckBoxBlock("climbed", "Robot successfully climbed (Second or third level)"), RadioButtonBlock("climbLevel", "What platform did the robot climb to?", 0, 1, 2, 3), CheckBoxBlock("brokeDown", "Robot tipped, broke down or lost COMMS"), IntBlock("ratePannels", "What would you rate the robot's ability to score hatch panels?(/10)", max=10), IntBlock("rateCargo", "What would you rate the robot's ability to score cargo?(/10)", max=10), IntBlock("rateRocketPanels", "What would you rate the robot's ability to score panels on rockets?(/10)", max=10), IntBlock("rateRocketCargo", "What would you rate the robot's ability to score cargo on rockets?(/10)", max=10), IntBlock("rateBot", "What would you rate the robot overall?(/10)", max=10), StringBlock("comments", "Comments")]

    return render_template('matchScouting.html', template=template)


@web.route('/scouting/submit', methods=['POST'])
@flask_login.login_required
def submitScouting():
    ScoutingWorker.saveData(4618, request.get_json())
    return redirect(url_for('matchScoutingPage'))


@web.route('/pit/')
def pitScoutingPage():
    return render_template('pitScouting.html')


@web.route('/picklist/')
def pickListPage():
    return render_template('picklist.html')


if __name__ == "__main__":
    loadUsers()
    serve(web, port=int(argv[1])if len(argv) > 1 else 5000)
    # web.run(debug=True)
