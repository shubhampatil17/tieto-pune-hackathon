import risk_constants

def get_status_risk(marital_status):
    if marital_status == "Married" :
        marital_risk = risk_constants.LOW_RISK
    else :
        marital_risk = risk_constants.MODERATE_RISK
    print "Marital Status : ",marital_risk
    return marital_risk


def get_age_risk(age):
    if age < 17:
        age_risk = risk_constants.NO_RISK
    elif age < 35:
        age_risk = risk_constants.MODERATE_RISK
    elif age < 60:
        age_risk =  risk_constants.LOW_RISK
    else :
        age_risk = risk_constants.HIGH_RISK
    print "Age Risk : ",age_risk
    return age_risk

def get_stay_risk(duration):
    if duration < 10 :
        stay_risk = risk_constants.LOW_RISK
    elif duration < 20 :
        stay_risk = risk_constants.MODERATE_RISK
    else :
        stay_risk = risk_constants.HIGH_RISK
    print "Duration of stay risk/ Total trip length risk : ",stay_risk
    return stay_risk

def get_trip_type_risk(type):
    if type == 1:
        type_risk = risk_constants.LOW_RISK
    elif type <= 3:
        type_risk = risk_constants.MODERATE_RISK
    else :
        type_risk = risk_constants.HIGH_RISK
    print "Trip Type Risk (Single/Maultiplt) : ",type_risk
    return type_risk