import geocoder
import requests
import api_endpoints
import database_connection
from models import Population
import risk_constants


def get_crime_data_date_span(months):
    response = requests.get(api_endpoints.uk_crime_data_availability_api_endpoint).json()
    return [x['date'] for x in response[:months]]


def fetch_crime_data(geocode, date=None):
    x0, y0 = str(geocode.bbox['southwest'][0]), str(geocode.bbox['southwest'][1])
    x1, y1 = str(geocode.bbox['northeast'][0]), str(geocode.bbox['northeast'][1])

    params = {
        'poly' : '{},{}:{},{}:{},{}:{},{}'.format(x0, y1, x0, y0, x1, y0, x1, y1),
        'date' : date
    }

    response = requests.post(api_endpoints.uk_crime_data_api_endpoint, params = params)

    if response.status_code == 503:
        return None

    return response.json()


def get_crime_risk_by_location(location):
    print('STATUS : Calculating crime risk for location {} ...'.format(location))
    geocode = geocoder.google(location)
    total_crimes = 0
    crime_categories = [
        'violent-crime',
        'robbery',
        'theft-from-the-person',
        'vehicle-crime',
        'bicycle-theft',
        'burglary',
        'criminal-damage-arson',
        'other-theft'
    ]

    for date in get_crime_data_date_span(12):
        crime_data = fetch_crime_data(geocode, date)
        if crime_data:
            for crime in crime_data:
                if 'category' in crime and crime['category'] in crime_categories:
                    total_crimes += 1
        else:
            total_crimes += 10000

    population = Population.objects(country = geocode.country.lower(), city = location.lower()).first().population
    crime_rate = (total_crimes/population)*1000

    if crime_rate > 200:
        risk = risk_constants.EXTREME_RISK
    elif crime_rate > 100:
        risk = risk_constants.HIGH_RISK
    elif crime_rate > 50:
        risk = risk_constants.MODERATE_RISK
    elif crime_rate > 20:
        risk = risk_constants.LOW_RISK
    else:
        risk = risk_constants.NO_RISK

    print('STATUS : Crime risk for {} is {}.'.format(location, risk))
    return risk