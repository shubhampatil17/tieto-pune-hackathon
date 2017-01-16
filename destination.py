from weather import *
from crime import *
from twitter_handler import *
from news_handler import *
import risk_constants
from datetime import datetime, timedelta

def get_destination_risk(destination, start_date):

    #get weather data

    date = datetime.now()
    yesterday = date - timedelta(days=1)
    lastday = date + timedelta(days=6)
    if yesterday.date() > start_date.date():
        return 0
    elif start_date.date() > lastday.date():
        weather_risk = get_approx_weather_risk(destination)
    else:
        weather_risk = get_weather_risk(destination, start_date)

    print "Weather Risk : ",weather_risk
    #get crime data
    crime_risk = get_uk_crime_risk(destination)
    print "Crime Risk : ",crime_risk

    #get twitter data
    #twitter_risk = percentage_of_crisis_tweets(destination)
    #print "Twitter Risk : ",twitter_risk

    #get news data
    news_risk = percentage_of_crisis_news(destination)
    print "News Risk : ", news_risk

    return int(weather_risk) + int(crime_risk) + int(2) + int(news_risk)