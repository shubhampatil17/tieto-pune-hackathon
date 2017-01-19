from twitter_stats import get_crisis_risk_from_twitter_by_location
from news_stats import get_crisis_risk_from_news_by_location
from crime_stats import get_crime_risk_by_location
from weather_stats import get_weather_risk_for_location
from personal_stats import *
from risk_constants import risk_status

def get_risk_for_place(location, start_date, duration):
    twitter_crisis_risk = get_crisis_risk_from_twitter_by_location(location)
    news_crisis_risk = get_crisis_risk_from_news_by_location(location)
    crime_risk = get_crime_risk_by_location(location)
    weather_risk = get_weather_risk_for_location(location=location, start_date=start_date, duration=duration)
    overall_risk = max(twitter_crisis_risk, news_crisis_risk, crime_risk, weather_risk)
    print('STATUS : Overall risk for the destination {} - {}'.format(location, risk_status[overall_risk]))
    return overall_risk


def get_aggregate_premium_rate_for_place(location, start_date, duration, age, marital_status):
    place_risk = 2 + (get_risk_for_place(location, start_date, duration)/5)*4 # 2% to 6%
    age_risk = 1 + (get_risk_by_age(age)/5)*2   # 1% to 3%
    marital_risk = 1 + (get_risk_by_marital_status(marital_status)/3)*1 # 1% to 2%
    print('STATUS : Calculated premium rate for destination {} - {} %'.format(location, place_risk + age_risk + marital_risk))
    return (place_risk + age_risk + marital_risk)/100
