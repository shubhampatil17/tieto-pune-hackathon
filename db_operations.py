from mongoengine import connect, Document, StringField, DateTimeField, ListField
from datetime import datetime
connect('test')

class Population(Document):
    country = StringField()
    city = StringField()
    population= StringField()

class Tweets(Document):
    location = StringField()
    timestamp = DateTimeField(default=datetime.now())
    tweets = ListField()

def save_tweets_in_db(location, tweets):
    tweets = Tweets(location = location, tweets = tweets)
    tweets.save()

def get_tweets_from_db(location):
    tweets_data = Tweets.objects(location = location)
    total_tweets = []
    if len(tweets_data) > 0:
        for item in tweets_data:
            total_tweets.append(item.tweets)

    return total_tweets

def get_population_from_db(location):
    population_data = Population.objects(city=location)
    return population_data[0].population
