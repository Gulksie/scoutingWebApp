from os import urandom
from sys import argv
from flask import Flask, render_template, make_response, request, url_for, redirect
import flask_login

from waitress import serve

from Classes.Block import *

# static vars

# app and login
web = Flask(__name__)
web.secret_key = urandom(16)
# loginManager = flask_login.LoginManager()
# loginManager.init_app(web)


@web.route('/')
@web.route('/home')
def home():
    return render_template('home.html')


# setup login
# TODO: USER AUTHENICATION, STORAGE, LIKE THE WHOLE LOGIN THING LOL
# https://flask-login.readthedocs.io/en/latest/#how-it-works
@web.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        return login()

    return render_template("login.html", retry=False)


def login():
    usr = request.form['usr']
    psw = request.form['psw']

    # TODO: not this...anything but this
    # this login is the equivalent of not having one at all
    if usr == "gulk" and psw == "geist":
        resp = redirect(url_for('home'))
        resp.set_cookie('loggedIn', "true")
        resp.set_cookie('usr', usr)
        return resp

    else:
        return render_template('login.html', retry=True)


@web.route('/scouting/')
def matchScoutingPage():
    return render_template('matchScouting.html', template=[StringBlock('str01', 'This is an example of a string input', 'Sample Text'),
                                                           IntBlock(
                                                               'int01', 'This is an example of a int input', default=1234, max=9999),
                                                           TallyIntBlock(
        'tally01', 'This is an example of a tally interger box', default=13),
        CheckBoxBlock('tally01', 'This is an example of a check box')])


@web.route('/pit/')
def pitScoutingPage():
    return render_template('pitScouting.html')


@web.route('/picklist/')
def pickListPage():
    return render_template('picklist.html')


if __name__ == "__main__":
    serve(web, port=int(argv[1])if len(argv) > 1 else 8000)
    # app.run()
