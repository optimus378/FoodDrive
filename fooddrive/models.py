from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from config import Config
import datetime

db = MongoEngine()

class Agent(db.Document):
    marketcenter = db.StringField(required=True)
    email = db.EmailField(required = True)
    firstname = db.StringField(max_length=50)
    lastname = db.StringField(max_length=50)
    bagnumber = db.IntField(max_value=2000, precision=0)
    streets = db.ListField()
    created_at = db.DateTimeField(default=datetime.datetime.now, editable=False,)
