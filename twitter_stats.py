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
            q=urllib.parse.quote('near:{} -RT'.format(location)),
            within="{}mi".format(radius),
            result_type='recent',
            # count=100,
            since=(datetime.now().date() - timedelta(days=3)).strftime('%Y-%m-%d'),
            until=(datetime.now().date()).strftime('%Y-%m-%d'),
            lang='en'
        ).items():
            tweets.append(tweet.text)

        # tweets_data = Tweets(location = location.lower(), tweets = tweets)
        # tweets_data.save()

    return tweets


def get_crisis_risk_from_twitter_by_location(location):
    print('STATUS : Analyzing Twitter ...')
    tweets = fetch_tweets_by_location(location)
    if len(tweets):
        informative_tweets_clf = ml_model.tweet_clf_extra.predict(tweets)
        informative_tweets = [tweets[x] for x in range(len(tweets)) if informative_tweets_clf[x] == 'Related and informative']
        crisis_tweets_clf = ml_model.tweet_clf.predict(informative_tweets)
        crisis_tweets = [informative_tweets[x] for x in range(len(informative_tweets)) if crisis_tweets_clf[x] == 'on-topic']
        stats = collections.Counter(crisis_tweets_clf)
        print(stats)
        print(crisis_tweets)
        on_topic = stats['on-topic'] if 'on-topic' in stats else 0
        crisis_tweets_percentage = (on_topic * 100)/(len(tweets))
        print('STATUS : Percentage of tweets from destination {} related to crisis - {}% '.format(location, crisis_tweets_percentage))
        if crisis_tweets_percentage > 80:
            risk = risk_constants.EXTREME_RISK
        elif crisis_tweets_percentage > 60:
            risk = risk_constants.HIGH_RISK
        elif crisis_tweets_percentage > 30:
            risk = risk_constants.MODERATE_RISK
        elif crisis_tweets_percentage > 5:
            risk = risk_constants.LOW_RISK
        else:
            risk = risk_constants.NO_RISK

    else:
        risk = risk_constants.LOW_RISK

    print('STATUS : Crisis (Twitter) risk at destination {} - {}'.format(location, risk_constants.risk_status[risk]))
    return risk

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