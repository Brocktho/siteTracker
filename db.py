from flask import Flask
from flask_pymongo import pymongo


client = pymongo.MongoClient("mongodb+srv://Brock:Rocketspaceship9126@sitetracker.g9j37.mongodb.net/SiteTracker?retryWrites=true&w=majority", port=27017)
db = client.get_database("SiteTracker")
user_collection = pymongo.collection.Collection(db, 'Websites')



