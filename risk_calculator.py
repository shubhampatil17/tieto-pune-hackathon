from twitter_stats import get_crisis_risk_from_twitter_by_location
from news_stats import get_crisis_risk_from_news_by_location
from crime_stats import get_crime_risk_by_location
from weather_stats import get_weather_risk_for_location

def get_risk_for_place(location, start_date, duration):
    twitter_crisis_risk = get_crisis_risk_from_twitter_by_location(location)
    news_crisis_risk = get_crisis_risk_from_news_by_location(location)
    crime_risk = get_crime_risk_by_location(location)
    weather_risk = get_weather_risk_for_location(location=location, start_date=start_date, duration=duration)

    return max(twitter_crisis_risk, news_crisis_risk, crime_risk, weather_risk)


def get_aggregate_risk_for_place(location, start_date, duration, age, marital_status)