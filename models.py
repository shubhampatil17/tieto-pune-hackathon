from mongoengine import Document, StringField, DateTimeField, IntField, ListField
from datetime import datetime

class Population(Document):
    country = StringField()
    city = StringField(required=True)
    population = IntField(required=True)

class Tweets(Document):
    location = StringField()
    timestamp = DateTimeField(default=datetime.now())
    tweets = ListField()

class New(Document):
    location = StringField()
    timestamp = DateTimeField(default=datetime.now())
    headlines = ListField()
