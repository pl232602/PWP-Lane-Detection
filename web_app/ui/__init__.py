import flask
from flask import render_template, redirect, url_for, request


root= flask.Blueprint("root",__name__)

@root.route("/",methods=["GET","POST"])
def submit():
    if flask.request.method=="POST":
        name=request.form["name"]
        pl=request.form["plnumber"]
        return render_template("confirm.html",content=name, contents=pl)
    return render_template("login.html")


@root.route("/re_enter",methods=["GET","POST"])
def re_enter():
    return render_template("re_enter.html")