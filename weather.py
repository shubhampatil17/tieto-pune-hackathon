import pyowm
from datetime import datetime, timedelta
import risk_constants
import access_tokens

condition = {risk_constants.NO_RISK: [800, 801, 951], risk_constants.LOW_RISK: [200, 600, 701, 711, 721, 731, 741, 751, 761], risk_constants.MODERATE_RISK: [201, 601, 961],
             risk_constants.HIGH_RISK: [221, 616, 602, 202, 212, 232, 511, 504, 622], risk_constants.EXTREME_RISK: [900, 901, 902, 903, 904, 905, 906]}


def get_approx_weather_risk(place):
    owm = pyowm.OWM(access_tokens.weather_access_token)
    fc = owm.daily_forecast(place)
    forecast = fc.get_forecast()
    total_risk = 0
    for weather in forecast:
        weather_code = weather.get_weather_code()
        flag = 1
        for risk, code in condition.items():
            if code == weather_code or isinstance(code, list) and weather_code in code:
                flag = 0
        if flag:
            risk = risk_constants.LOW_RISK
        total_risk = total_risk + risk
    return total_risk / 7


def get_weather_risk(place, date):
    default_risk = risk_constants.LOW_RISK
    try:
        owm = pyowm.OWM(access_tokens.weather_access_token)
        fc = owm.daily_forecast(place)
        weather = fc.get_weather_at(date)
        weather_code = weather.get_weather_code()
        print "Weather Code ",weather_code
        flag = 1
        for risk, code in condition.items():
            if code == weather_code or isinstance(code, list) and weather_code in code:
                flag = 0
                return risk
    except :
        print "JSON format error"
    return default_risk

def trial_weather_data():
    API_KEY = '65b093b8f06e18e183b0b871142ef37f'
    owm = pyowm.OWM(API_KEY)
    # https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md
    obs = owm.weather_at_places('London,uk', searchtype='like')  # Toponyim searchtype='accurate',like
    obs = owm.weather_at_id(2643741)  # City ID
    obs = owm.weather_at_coords(-0.107331, 51.503614)  # lat/lon
    fc = owm.daily_forecast('London,uk')
    f = fc.get_forecast()
    date = datetime.strptime('Jan 11 2017  1:33PM', '%b %d %Y %I:%M%p')
    date = datetime.now()
    date_wise = fc.get_weather_at(date)
    # How many weather items are in the forecast?
    items = len(f)
    f.get_location()
    for weather in f:
        weather_code = weather.get_weather_code()
        print (weather.get_reference_time('iso'), weather.get_status())
        print "Humidity : " + str(weather.get_humidity())
        print "Wind : " + str(weather.get_wind())
        print "Temperature : " + str(weather.get_temperature('celsius'))
        print "Cloud Average : " + str(weather.get_clouds())
        print "Rain : " + str(weather.get_rain())
        print "Snow : " + str(weather.get_snow())
        print " Pressure : " + str(weather.get_pressure())

        # ('2017-01-13 12:00:00+00', u'Rain')
        # ('2017-01-14 12:00:00+00', u'Clear')


