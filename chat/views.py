from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from flask_login.utils import login_required
from flask import globals as g, redirect

from chat import controller
from chat.app import app
from chat.exceptions import ValidationError


@app.route("/")
@login_required
def index():
    return redirect(url_for("chat"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    next = g.request.args.get('next')
    if g.request.method == "POST":
        try:
            controller.login(g.request.form.get("username"))
            return redirect(next or url_for("index"))
        except ValidationError as e:
            error = e

    return render_template("login.html", error=error)


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    error = None

    history = controller.history()

    if request.method == "POST":
        message = request.form["message"]

        try:
            controller.new_message(message)
            return redirect(url_for("chat"))
        except ValidationError as e:
            error = e

    return render_template("chat.html", error=error, messages=history)
