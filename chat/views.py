from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import logout_user
from flask_login.utils import login_required
from flask import globals as g, redirect, jsonify

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


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/chat", methods=["GET"])
@login_required
def chat():
    return render_template("chat.html")


@app.route("/api/chat/history")
@login_required
def api_chat_history():
    data = []

    for h in controller.history():
        item = h.to_dict()
        # history calls fetch_users - so all users are prefetched
        item["user"] = h.user.fetch().to_dict()
        data.append(item)

    return jsonify(data)
