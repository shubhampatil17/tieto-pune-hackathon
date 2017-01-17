
import geocoder
import requests
import api_endpoints
import database_connection
from models import Population
from datetime import datetime
# from __future__ import division
# import requests
# import json
# import risk_constants
# import geocoder
# import access_tokens
# import api_endpoints
# import db_operations
#
# def get_indian_crime_data():
#     payload = {'resource_id': '5bc0be8a-69e5-4a23-9d8c-163924f143e7', 'api-key': access_tokens.india_crime_access_token}
#     r = requests.get(api_endpoints.india_crime_data_api_endpoint, params=payload)
#     data = r.text
#     status = r.status_code
#     try:
#         decoded = json.loads(data)
#         print(decoded['records'][1])
#         for record in decoded['records']:
#             if record['State/ UTs'] == "TOTAL (STATES)" and record['Crime Head'] == "TOTAL CRIMES AGAINST WOMEN":
#                 print record
#             #	if record['Crime Head'] == "TOTAL CRIMES AGAINST WOMEN":
#             #		print record
#             #		print "hi"
#     except (ValueError, KeyError, TypeError):
#         print "Indian Crime : JSON format error"
#
#
#
# def get_uk_crime_data(payload):
#     possible_crimes = {'bicycle-theft': 0, 'burglary': 0, 'other-theft': 0, 'possession-of-weapons': 0,
#                        'vehicle-crime': 0}
#     r = requests.get(api_endpoints.uk_crime_data_api_endpoint, params=payload)
#     total = 0
#     try:
#         sub_total = 0
#         data = json.loads(r.text)
#         total = len(data)
#         for record in data:
#             category = record['category']
#             if category in possible_crimes:
#                 sub_total += 1
#         #         possible_crimes[category] += 1
#         # total=0
#         # for key, value in possible_crimes.items():
#         #     total += value
#     except (ValueError, KeyError, TypeError):
#         print "JSON format error"
#         return 0,0
#     return total,sub_total
#
#
# #get_uk_crime_risk("Encamp")

# def get_uk_crime_risk(place):
#     #box = {'northeast': [52.268, 0.543], 'southwest': [52.794, 0.238]}
#     box = geocoder.google(place).bbox
#     x1 = str(box['northeast'][0])
#     y1 = str(box['northeast'][1])
#     x2 = str(box['southwest'][0])
#     y2 = str(box['southwest'][1])
#     dates = ['2015-02','2015-03','2015-04']
#     total_crime = 0
#     possible_crime = 0
#     for date in dates:
#         payload = {'poly': x1 + ',' + y1 + ':' + x1 + ',' + y2 + ':' + x2 + ',' + y2 + ':' + x2 + ',' + y1, 'date': date}
#         total_crime1, possible_crime1 = get_uk_crime_data(payload)
#         total_crime += total_crime1
#         possible_crime += possible_crime1
#
#     print total_crime,possible_crime
#     population = 40000
#     # population = int(db_operations.get_population_from_db(place))
#     if population != 0 and possible_crime != 0:
#         print "Crime Risk :", population/possible_crime
#         factor = population/possible_crime
#         if factor < 3:
#             return risk_constants.LOW_RISK
#         elif factor < 15 :
#             print risk_constants.MODERATE_RISK
#         else :
#             return risk_constants.HIGH_RISK
#     return risk_constants.LOW_RISK

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
    geocode = geocoder.google(location)
    total_crimes = 0

    for date in get_crime_data_date_span(12):
        crime_data = fetch_crime_data(geocode, date)
        for crime in crime_data:
            print(crime)
    #     total_crimes += len(crime_data) if crime_data else 10000
    #
    # population = Population.objects(country = geocode.country.lower(), city = location.lower()).first().population
    # crime_rate = (total_crimes/population)*1000
    # print("population", population)
    # print("crimes", total_crimes)
    # print("rate", crime_rate)

get_crime_risk_by_location('oxford')
