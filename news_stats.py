import webhose
import access_tokens
from datetime import datetime, timedelta
import ml_model
import geocoder
import collections
import risk_constants

webhose.config(token=access_tokens.webhose_access_token)

def fetch_news_by_location(location):
    geocode = geocoder.google(location)
    query = {
        'location': location,
        'language': 'english',
        'site_type': 'news',
        'thread.country':geocode.country,
    }

    headlines = [x.title for x in webhose.search(query=query, since=int((datetime.now() - timedelta(days=3)).strftime("%s")))]
    return headlines


def get_crisis_risk_from_news_by_location(location):
    headlines = fetch_news_by_location(location)
    if len(headlines):
        informative_news_clf = ml_model.tweet_clf_extra.predict(headlines)
        informative_news = [headlines[x] for x in range(len(headlines)) if informative_news_clf[x] == 'Related and informative']
        crisis_news_clf = ml_model.tweet_clf.predict(informative_news)
        crisis_news = [informative_news[x] for x in range(len(informative_news)) if crisis_news_clf[x] == 'on-topic']
        stats = collections.Counter(crisis_news_clf)
        on_topic = stats['on-topic'] if 'on-topic' in stats else 0
        crisis_news_percentage = (on_topic * 100)/(len(headlines))
        for news in informative_news:
            print(news)
        print(stats)
        for news in crisis_news:
            print(news)
        print(crisis_news_percentage)
        if crisis_news_percentage > 60:
            risk = risk_constants.HIGH_RISK
        elif crisis_news_percentage > 30:
            risk = risk_constants.MODERATE_RISK
        else:
            risk = risk_constants.LOW_RISK

    else:
        risk = risk_constants.LOW_RISK

    return risk