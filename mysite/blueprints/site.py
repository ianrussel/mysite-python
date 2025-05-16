from flask import Blueprint, jsonify, render_template, request

from mysite.backend.core import run_llm

site_blueprint = Blueprint("site_blueprint", __name__)


@site_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@site_blueprint.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    chat_history = data.get("history", [])

    response = run_llm(query=prompt, chat_history=chat_history)
    return jsonify(
        {
            "answer": response["answer"],
            # "sources": sources_str,
        }
    )
