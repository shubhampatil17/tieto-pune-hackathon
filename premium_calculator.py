from risk_calculator import get_aggregate_premium_rate_for_place
from datetime import datetime


def preprocess_trip_plan(trip_plan):
    if 'trip_schedule' in trip_plan and 'age' in trip_plan and 'marital_status' in trip_plan and 'trip_cost' in trip_plan:
        for x in range(len(trip_plan['trip_schedule'])):
            trip_plan['trip_schedule'][x]['start_date'] = datetime.strptime(trip_plan['trip_schedule'][x]['start_date'], '%Y-%m-%dT%H:%M:%S')

        print(trip_plan)

        for x in range(len(trip_plan['trip_schedule']) - 1):
            trip_plan['trip_schedule'][x]['duration'] = int((trip_plan['trip_schedule'][x+1]['start_date'] - trip_plan['trip_schedule'][x]['start_date']).days)
            response = True
    else:
        response = False

    return response, trip_plan


def calculate_premium_for_trip(trip_plan):
    response, trip_plan = preprocess_trip_plan(trip_plan)

    print('STATUS : Your trip plan is as follows ...')

    print('DATA : Trip plan')
    for trip in trip_plan['trip_schedule'][:-1]:
        print(trip)

    print('DATA : Age - {}'.format(trip_plan['age']))
    print('DATA : Marital Status - {}'.format(trip_plan['marital_status']))
    print('DATA : Trip cost - {}'.format(trip_plan['trip_cost']))

    if response:
        total_days_of_trip = 0
        premium_rate_per_destination = []

        for trip in trip_plan['trip_schedule'][:-1]:
            total_days_of_trip += trip['duration']
            premium_rate_per_destination.append(get_aggregate_premium_rate_for_place(
                trip['destination'],
                trip['start_date'],
                trip['duration'],
                trip_plan['age'],
                trip_plan['marital_status']
            ))

        cost_per_day_per_destination = trip_plan['trip_cost']/(total_days_of_trip*(len(trip_plan['trip_schedule'])-1))
        premium_per_destination = [cost_per_day_per_destination * trip_plan['trip_schedule'][x]['duration'] * premium_rate_per_destination[x] for x in range(len(trip_plan['trip_schedule'])-1)]
        print('STATUS : Premium distribution per destination')
        print(premium_per_destination)
        print('STATUS : CUSTOMIZED PREMIUM FOR COMPLETE TRIP - {}'.format(sum(premium_per_destination)))

    else:
        print('EXCEPTION : Cannot proceed. Missing details in trip plan')
        print('REQUIRED : TRIP SCHEDULE, AGE, MARITAL STATUS, TRIP COST')

    return sum(premium_per_destination)