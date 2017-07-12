from flask import Blueprint
from flask import render_template, request
from webapp.hello.models import MESSAGES

hello = Blueprint("hello", __name__)


@hello.route("/")
@hello.route("/hello")
def hello_world():
    user = request.args.get("user", "Shalabh")
    return render_template("index.html", user=user)

@hello.route("/show/<key>")
def get_message(key):
    return MESSAGES.get(key) or "{0} not found!".format(key)

@hello.route("/add/<key>/<message>")
def add_or_update_message(key, message):
    MESSAGES[key] = message
    return "{0} Added/Updated".format(key)

