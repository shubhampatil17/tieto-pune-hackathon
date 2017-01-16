import tweepy
import access_tokens
import geocoder
from datetime import datetime, timedelta
import db_operations
import ml_model
import collections
import risk_constants

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

auth = tweepy.AppAuthHandler(access_tokens.tweepy_consumer_key, access_tokens.tweepy_secret_key)
twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_geocode(location):
    return geocoder.google(location)


def get_tweets(location):
    geocode = get_geocode(location)
    geocodes = "{},{}".format(geocode.latlng[0], geocode.latlng[1])
    radius = '150km'
    tweets = []
    try:
        # for tweet in tweepy.Cursor(
        #             twitter_api.search, q=location,
        #             result_type='recent',
        #             #count = 200,
        #             since = (datetime.now().date()-timedelta(days=2)).strftime('%Y-%m-%d'),
        #             until = (datetime.now().date()).strftime('%Y-%m-%d'),
        #             lang = 'en'
        #         ).items(100):
        #
        #     tweets.append(tweet.text)

        tweets = db_operations.get_tweets_from_db(location)
        if len(tweets) == 0:
            for tweet in tweepy.Cursor(
                        twitter_api.search,
                        geocode= geocodes + ',' + radius,
                        result_type='recent',
                        #count = 200,
                        since = (datetime.now().date()-timedelta(days=2)).strftime('%Y-%m-%d'),
                        until = (datetime.now().date()).strftime('%Y-%m-%d'),
                        lang = 'en'
                    ).items(100):

                tweets.append(tweet.text)

            db_operations.save_tweets_in_db(location, tweets)
    except:
        pass

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
