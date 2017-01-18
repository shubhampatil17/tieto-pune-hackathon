import pyowm
from datetime import datetime, timedelta
import risk_constants
import access_tokens

weather_condition_categories = {
    risk_constants.EXTREME_RISK: [900, 901, 902, 903, 904, 905, 906, 962, 781],
    risk_constants.HIGH_RISK: [961, 959, 622, 504, 503, 502, 314, 312, 302, 232, 212],
    risk_constants.MODERATE_RISK: [960, 958, 957, 762, 621, 616, 602, 531, 522, 511, 501, 321, 313, 311, 301, 231, 230, 221, 211, 202, 201],
    risk_constants.LOW_RISK: [956, 804, 803, 802, 771, 761, 751, 741, 731, 721, 620, 615, 612, 611, 601, 521, 520, 500, 310, 300, 210, 200],
    risk_constants.NO_RISK: [955, 954, 953, 952, 951, 801, 800, 711, 701, 600]
}

owm = pyowm.OWM(access_tokens.weather_access_token)


def get_weather_risk_for_location(location, start_date, duration):
    forecaster = owm.daily_forecast(location)
    forecast = forecaster.get_forecast()
    # forecast_start_date = datetime.now() - timedelta(days=1)
    forecast_end_date = datetime.now() + timedelta(days=5)
    trip_start_date = start_date
    trip_end_date = start_date + timedelta(days=duration)

    if trip_start_date > forecast_end_date:
        weathers = [weather.get_weather_code() for weather in forecast.get_weathers()]
    else:
        weathers = [forecaster.get_weather_at(start_date + timedelta(days=day)).get_weather_code() for day in range(int(((trip_end_date if trip_end_date < forecast_end_date else forecast_end_date) - trip_start_date).days) + 1)]

    weathers_risks = [y for x in weathers for y in weather_condition_categories if x in weather_condition_categories[y]]
    return max(weathers_risks)

get_weather_risk_for_location('oxford', datetime(2017, 1, 22), 1)