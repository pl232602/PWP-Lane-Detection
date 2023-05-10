import flask
import hashlib
from flask import render_template, redirect, url_for, request
from loginapi import user


root= flask.Blueprint("root",__name__)

@root.route("/",methods=["GET","POST"])
def submit():
    if flask.request.method=="POST":
        name=request.form["username"] #Take user input from webpage.
        pl=request.form["password"]

        #Inputted usname and password combination will be hashed here, and the logapi file userapi file will be used to check if a hashed copy exists in the user database.

        return render_template("webapp.html",content=name, contents=pl)
    return render_template("login.html")

@root.route("/create_user",methods=['GET','POST'])
def create_user():
    if request.method=="POST":
        adduser=user([request.form["username"],request.form["password"]])
        print([request.form["username"],request.form["password"]])
        adduser.credential_hash()
        adduser.add_user()
        if adduser.add_user() == False:
            return render_template("user_exists.html")
        else:
            return render_template("user_created.html")
    return render_template("create_user.html")

@root.route("/user_exists",methods=["GET","POST"])
def user_exists():
    if request.method=="POST":
        return render_template("create_user.html")