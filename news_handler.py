import webhose
import access_tokens
from datetime import datetime, timedelta
import time
import ml_model
import collections
import risk_constants
webhose.config(token=access_tokens.webhose_access_token)

def get_news_headlines(location):
    query = {
        'location': location,
        'language': 'english',
        'latest' : True,
        'site_type' : 'news'
    }

    news = webhose.search(query=query, since=datetime.now() - timedelta(days=2))
    latest_headlines = []

    # while len(latest_headlines) < 200:
    for each_news in news:
        latest_headlines.append(each_news.title)
            # news = news.get_next()

    return latest_headlines


def percentage_of_crisis_news(location):
    news = get_news_headlines(location)
    informative_prediction = ml_model.tweet_clf_extra.predict(news)
    filtered_news = []

    for i in range(len(informative_prediction)):
        if informative_prediction[i] == 'Related and informative':
            filtered_news.append(news[i])

    crisis_prediction = ml_model.tweet_clf.predict(filtered_news)
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
