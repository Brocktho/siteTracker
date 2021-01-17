from flask import Flask
from db import user_collection
import os

def create_app(testing=False):
    # loads testing config if true, else loads and returns Flask App

    SiteTrackerDb = Flask(__name__)
    db = user_collection

    # unused currently, was trying to set up different environments, but the 
    # .util file is something i don't understand at this moment, so we have unused variable here.
    flask_env = os.getenv("FLASK_ENV", None)

    from SiteTrackerDb.routes import view
    SiteTrackerDb.register_blueprint(view)

    return SiteTrackerDb