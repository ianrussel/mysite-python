import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

# Read your API key from .env
API_KEY = os.getenv("REQUEST_API_KEY")

#  Decorator to require API key
def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper