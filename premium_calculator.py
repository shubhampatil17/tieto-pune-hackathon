from destination import get_destination_risk
from risk_calculator import get_stay_risk
from risk_calculator import get_trip_type_risk
from risk_calculator import get_status_risk
from risk_calculator import get_age_risk
import risk_constants
from datetime import datetime

def calculate_risk(type, duration, destination, age, marital_status, start_date):
    destination_risk = get_destination_risk(destination,start_date)
    if  destination_risk>= risk_constants.EXTREME_RISK :
        return risk_constants.HIGH_PREMIUM
    total_risk = get_trip_type_risk(type) + get_stay_risk(duration) + destination_risk + get_status_risk(marital_status) + get_age_risk(age)
    return total_risk

#Input will be dict
#Eg, {'Type':1,'Stay':10,'Age':25,'Status':'Married', 'Destination': 'London,uk', 'Start_Date':datetime object, 'Total_Cost_of_Trip':20000, 'Cost_of_Premium':20000}

def premium_calculator(data):
    total_risk=0
    type=len(data)
    for client_data in data:
        total_risk += calculate_risk(client_data['Type'],client_data['Stay'],client_data['Destination'],client_data['Age'], client_data['Status'], client_data['Start_Date'])
        print "Total Risk", total_risk
    total_risk/=type

    if total_risk >= 35 or total_risk == risk_constants.HIGH_PREMIUM:
        #10%
        premium_amount=client_data['Cost_of_Premium']*0.10
    if total_risk >= 28:
        #8%
        premium_amount=client_data['Cost_of_Premium']*0.08
    if total_risk >= 22:
        #7%
        premium_amount=client_data['Cost_of_Premium']*0.07
    if total_risk >= 16:
        #6%
        premium_amount=client_data['Cost_of_Premium']*0.06
    if total_risk >= 11:
        #4%
        premium_amount=client_data['Cost_of_Premium']*0.04
    else:
        #3%
        premium_amount = client_data['Cost_of_Premium'] * 0.03
    print "Premium Amount",premium_amount
    return premium_amount

client_data = [{'Type':2,'Stay':10,'Age':25,'Status':'Married', 'Destination': "Totton", 'Start_Date':datetime.now(), 'Total_Cost_of_Trip':20000, 'Cost_of_Premium':20000},{'Type':2,'Stay':10,'Age':25,'Status':'Married', 'Destination': "Royal Tunbridge Wells", 'Start_Date':datetime.now(), 'Total_Cost_of_Trip':20000, 'Cost_of_Premium':20000}]

premium_calculator(client_data)