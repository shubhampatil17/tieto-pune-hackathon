import pandas as pd
import database_connection
from models import Population, Tweets

def create_population_dataset():
    if not len(Population.objects):
        print("STATUS : Loading population dataset into database ...")
        dataframe = pd.read_csv('population.csv', encoding="ISO-8859-1")
        for index, row in dataframe.iterrows():
            try:
                population = Population(country=row[0].lower(), city=row[1].lower(), population=int(row[4]))
                population.save()
            except:
                print("EXCEPTION : Error at row {}.".format(index))
        print("STATUS : Loading complete !")


def fetch_tweets_from_db(location):
    tweets_data = Tweets.objects(location = location.lower()).first()
    return tweets_data.tweets if tweets_data else None

def save_tweets_in_db(location, tweets):
    tweets_data = Tweets(location = location.lower(), tweets = tweets)
    tweets_data.save()
