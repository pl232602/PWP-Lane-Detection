import flask
import hashlib
from flask import render_template, redirect, url_for, request
from loginapi import user


root= flask.Blueprint("root",__name__)

current_user = "null"

@root.route("/",methods=["GET","POST"]) #login page
def submit():
    if flask.request.method=="POST":
        username=request.form["username"] #Take user input from webpage.
        current_user = username
        password=request.form["password"]
        checkuser=user([request.form["username"],request.form["password"]]) #check if user is in the database
        if checkuser.check_user() == True:
            return render_template("index.html", session_user = current_user) #if the user is in database, display main page
        else:
            print("login failed") #if user is not in database, do not show main page


        #Inputted usname and password combination will be hashed here, and the logapi file userapi file will be used to check if a hashed copy exists in the user database.

    return render_template("login.html")

@root.route("/create_user",methods=['GET','POST'])
def create_user():
    if request.method=="POST":
        adduser=user([request.form["username"],request.form["password"]]) #get input from user
        print([request.form["username"],request.form["password"]])
        adduser.credential_hash() #hash credentials using cryptographically secure methods
        if adduser.add_user() == False:
            return render_template("user_exists.html") #if user with matching username exists, notify user
        else:
            adduser.add_user() #ifstching username doesnt exist, notify user of successful credential creation 
            return render_template("user_created.html")
    return render_template("create_user.html")

@root.route("/user_exists",methods=["GET","POST"])
def user_exists():
    if request.method=="POST":
        return render_template("create_user.html") #return user to user creation 