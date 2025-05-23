# Standard Library

from flask import Flask
from flask_cors import CORS

from mysite.blueprints import site


# Function to create and configure the Flask application instance
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(site.site_blueprint)

    # Return the configured application instance
    return app


# Instantiate the Flask application by calling create_app
app = create_app()
CORS(app=app)