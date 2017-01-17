import tweepy
import access_tokens
import geocoder
import urllib
from geopy.distance import vincenty
from datetime import datetime, timedelta
import database_connection
import ml_model
import collections
import risk_constants
from models import Tweets

auth = tweepy.AppAuthHandler(access_tokens.tweepy_consumer_key, access_tokens.tweepy_secret_key)
twitter_handler = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def fetch_tweets_by_location(location):
    geocode = geocoder.google(location)
    radius = vincenty(tuple(geocode.bbox['northeast']), tuple(geocode.bbox['southwest'])).miles

    tweets_data = Tweets.objects(location = location.lower()).first()
    if tweets_data:
        tweets = tweets_data.tweets
    else:
        tweets = []
        for tweet in tweepy.Cursor(
            twitter_handler.search,
            q=urllib.parse.urlencode({
                "near" : location
            }),
            within="{}mi".format(radius),
            # result_type='recent',
            count=100,
            since=(datetime.now().date() - timedelta(days=7)).strftime('%Y-%m-%d'),
            until=(datetime.now().date()).strftime('%Y-%m-%d'),
            lang='en'
        ).items():
            tweets.append(tweet.text)

        # tweets_data = Tweets(location = location.lower(), tweets = tweets)
        # tweets_data.save()

    print(len(tweets))
    return tweets

def percentage_of_crisis_tweets(location):
    tweets = get_tweets(location)
    informative_prediction = ml_model.tweet_clf_extra.predict(tweets)
    filtered_tweets = []

    for i in range(len(informative_prediction)):
        if informative_prediction[i] == 'Related and informative':
            filtered_tweets.append(tweets[i])

    crisis_prediction = ml_model.tweet_clf.predict(filtered_tweets)
    stats = collections.Counter(crisis_prediction)
    on_topic = stats['on-topic'] if 'on-topic' in stats else 0
    off_topic = stats['off-topic'] if 'off-topic' in stats else 0

    risk_percentage = (on_topic * 100)/(on_topic + off_topic)

    if risk_percentage > 60:
        risk = risk_constants.HIGH_RISK
    elif risk_percentage > 30 and risk_percentage < 60:
        risk = risk_constants.MODERATE_RISK
    else:
        risk = risk_constants.LOW_RISK

    return risk
    # heuristically_filtered_tweets = []
    # for i in range(len(classified_tweets)):
    #     if classified_tweets[i] == 'on-topic':
    #         heuristically_filtered_tweets.append(tweets[i])


crisis_keywords = [
    'bridge',
    'intersection',
    'car',
    'bus',
    'truck',
    'vehicle',
    'evacuation',
    'evacuate',
    'fire',
    'police',
    'institution',
    'wind',
    'impact',
    'injured',
    'damage',
    'road',
    'airplane',
    'hospital',
    'school',
    'home',
    'building',
    'flood',
    'collapse',
    'death',
    'casualty',
    'missing'
]

fetch_tweets_by_location('oxford')
