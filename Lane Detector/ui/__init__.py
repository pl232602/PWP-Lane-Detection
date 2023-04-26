import flask
import hashlib
from flask import render_template, redirect, url_for, request


root= flask.Blueprint("root",__name__)

@root.route("/",methods=["GET","POST"])
def submit():
    if flask.request.method=="POST":
        name=request.form["username"] #Take user input from webpage.
        pl=request.form["password"]

        #Inputted usname and password combination will be hashed here, and the logapi file userapi file will be used to check if a hashed copy exists in the user database.

        return render_template("webapp.html",content=name, contents=pl)
    return render_template("login.html")


@root.route("/re_enter",methods=["GET","POST"])
def re_enter():
    return render_template("re_enter.html")