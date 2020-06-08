from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase

routing = Blueprint("routes", __name__)

#Global Constants
NAME_KEY = 'name'
MSG_LIMIT = 50

#Routes

@routing.route("/login", methods = ["POST", "GET"])
def login():
    """
    display the Login Screen and handle name joining the session
    except POST
    return none
    """
    if request.method == "POST": #user input name
        name = request.form["inputName"]
        if len(name) >= 3:
            session[NAME_KEY] = name
            flash(f'{name} has sucessfully logged in')
            return redirect(url_for("routes.home"))
        else:
            flash("Name must be longer than 2 characters")
    
    return render_template("login.html", **{"session": "session"})

@routing.route("/logout")
def logout():
    """
    Logout current user
    return none
    """
    session.pop(NAME_KEY, None)
    flash("You have sucesfully logged out")
    return redirect(url_for("routes.login"))

@routing.route("/")
@routing.route("/home")
def home():
    """
    Home page after the user logs in
    return none
    """
    if NAME_KEY not in session:
        return redirect(url_for("routes.login"))

    return render_template("index.html", **{"session": "session"})

@routing.route("/history")
def history():
    """
    Get the chat history
    """
    if NAME_KEY not in session:
        flash("You need to login before seeing chat history")
        return redirect(url_for("routes.login"))

    json_messages = get_history(session[NAME_KEY])
    print(json_messages)
    return render_template("history.html", **{"history": json_messages})

@routing.route("/get_name")
def get_name():
    """
    return the name of the logged in user as json object 
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)

@routing.route("/get_messages")
def get_messages():
    """
    Get all the messages stored in Database
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)

    return jsonify(messages)

def get_history(name):
    """
    Param: name
    Get the chat history of the user
    """
    db = DataBase()
    msgs = db.get_messages_by_user(name)
    messages = remove_seconds_from_messages(msgs)

    return messages

# SERVICES
def remove_seconds_from_messages(msgs):
    """
    Removes the seconds from messages
    param: message list
    return messages
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return messages

def remove_seconds(msg):
    """
    remove seconds 
    """
    return msg.split(".")[0][:-3]