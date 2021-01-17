from flask import Flask

import os

def create_app(testing=False):
    # loads testing config if true, else loads and returns Flask App

    app = Flask(__name__)

    # unused currently, was trying to set up different environments, but the 
    # .util file is something i don't understand at this moment, so we have unused variable here.
    flask_env = os.getenv("FLASK_ENV", None)

    with app.app_context():
        from SiteTrackerDb.SiteTracker import view
        app.register_blueprint(view)

    return app