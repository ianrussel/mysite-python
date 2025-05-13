from flask import Blueprint, render_template

site_blueprint = Blueprint("site_blueprint", __name__)


@site_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")
