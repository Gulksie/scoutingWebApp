from flask import Flask, render_template
web = Flask(__name__)


@web.route('/')
def helloWorld():
    return "Scouting...Under development"

@web.route('/login')
def login():
    return render_template("login.html")
