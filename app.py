from os import urandom, environ
from sys import argv

from flask import Flask, render_template, make_response, request, url_for, redirect, abort
import flask_login

from waitress import serve

from Classes.Block import *
from Classes.User import User, getUser, getGUser, addUser, loadUsers, saveUsers

# static vars

# app and login
web = Flask(__name__)
web.secret_key = urandom(16)
print('SECRET KEY:' + str(web.secret_key))

googleID = environ.get("GCID")  # THIS SHOULD BE AN ENVIORMENT VARIBLE

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


# setup login
# TODO: USER AUTHENICATION, STORAGE, LIKE THE WHOLE LOGIN THING LOL
# https://flask-login.readthedocs.io/en/latest/#how-it-works
@web.route('/login', methods=['GET', 'POST'])
def loginPage():
    if flask_login.current_user.is_authenticated:
        return abort(403)

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

    return render_template("login.html", retry=False, googleID=googleID)


def googleLogin():
    json = request.get_json()

    user = getGUser(json['ID'])

    if user == None:
        user = User(json['name'], json['email'], json['ID'])

    addUser(user)

    flask_login.login_user(user)

    saveUsers()

    return redirect(url_for('home'))


def login():

    usr = request.form.get('usr')
    psw = request.form.get('psw')

    # TODO: not this...anything but this
    # this login is the equivalent of not having one at all
    if usr == "gulk" and psw == "geist":
        resp = redirect(url_for('home'))
        resp.set_cookie('loggedIn', "true")
        resp.set_cookie('usr', usr)
        return resp

    else:
        return render_template('login.html', retry=True, googleID=googleID)


@web.route('/scouting/')
def matchScoutingPage():
    return render_template('matchScouting.html', template=[HeaderBlock("This is an example of a header"), StringBlock('str01', 'This is an example of a string input', 'Sample Text'),
                                                           IntBlock(
                                                               'int01', 'This is an example of a int input', default=1234, max=9999), SpaceBlock(50),
                                                           TallyIntBlock(
        'tally01', 'Above is a space, this is an example of a tally interger box', default=13),
        CheckBoxBlock('chck01', 'This is an example of a check box'), RadioButtonBlock('rdo01', "This is an example of a radio button input", 'Choice1', "Choice2", "Choice3")])


@web.route('/pit/')
def pitScoutingPage():
    return render_template('pitScouting.html')


@web.route('/picklist/')
def pickListPage():
    return render_template('picklist.html')


if __name__ == "__main__":
    loadUsers()
    #serve(web, port=int(argv[1])if len(argv) > 1 else 5000)
    web.run(debug=True)
