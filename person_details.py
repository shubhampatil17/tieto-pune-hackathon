import json
from datetime import datetime
import dateutil.parser

def format(datte):
    details = []
    try:
        travel_dates = sorted(datte['tripPlan'].values())
        journey_start_date = dateutil.parser.parse(str(travel_dates[0]))
        it = iter(travel_dates)
        destinations = datte['tripPlan'].keys()
        person_data={}
        if(len(destinations)==1):
            for k in destinations:
                print(k)
            person_data = {
                'Type': '1',
                'Stay': 1,
                'age': str(datte.get('age')),
                'Status': str(datte.get('marital_status')),
                'Destination': str(k),
                'Total_Cost_of_Trip': str(datte.get('Total_Cost_of_Trip')),
                'Cost_of_Premium': str(datte.get('Cost_of_Premium')),
                'Start_Date': journey_start_date
            }
        else:


            stay_arr = []
            for date in it:
                end_date = dateutil.parser.parse(str(next(it)))
                start_date = dateutil.parser.parse(str(date))
                stay = end_date - start_date
                stay_arr.append(stay)
            for st, dest in zip(stay_arr, destinations):
                person_data = {
                    'Type': '1',
                    'Stay': abs(st),
                    'age': str(datte.get('age')),
                    'Status': str(datte.get('marital_status')),
                    'Destination': str(dest),
                    'Total_Cost_of_Trip': str(datte.get('Total_Cost_of_Trip')),
                    'Cost_of_Premium': str(datte.get('Cost_of_Premium')),
                    'Start_Date': journey_start_date
                }

        details.append(person_data)
        return details
    except:
        pass
