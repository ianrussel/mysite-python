from flask import Blueprint, jsonify, render_template, request
from mysite.backend.core import run_llm
from mysite.cors import require_api_key

site_blueprint = Blueprint("site_blueprint", __name__)


@site_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@site_blueprint.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    chat_history = data.get("history", [])

    response = run_llm(query=prompt, chat_history=chat_history, index_name='resume-index', has_custom_prompt = True)
    return jsonify(
        { 
            "answer": response["answer"],
            # "sources": sources_str,
        }
    )

@site_blueprint.route("/api/chat2", methods=["POST"])
@require_api_key
def chat_2():
    data = request.json
    prompt = data.get("prompt", "")
    chat_history = data.get("history", [])

    response = run_llm(query=prompt, chat_history=chat_history, index_name='timetracking-index')
    return jsonify(
        {
            "answer": response["answer"],
            # "sources": sources_str,
        }
    )
