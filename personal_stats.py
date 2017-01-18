import risk_constants


def get_risk_by_marital_status(status):
    risk = risk_constants.LOW_RISK if status.lower() == "married" else risk_constants.MODERATE_RISK
    return risk


def get_risk_by_age(age):
    if age < 17:
        risk = risk_constants.NO_RISK
    elif age < 35:
        risk = risk_constants.LOW_RISK
    elif age < 60:
        risk = risk_constants.MODERATE_RISK
    else:
        risk = risk_constants.HIGH_RISK

    return risk

#
# def get_stay_risk(duration):
#     if duration < 10 :
#         stay_risk = risk_constants.LOW_RISK
#     elif duration < 20 :
#         stay_risk = risk_constants.MODERATE_RISK
#     else :
#         stay_risk = risk_constants.HIGH_RISK
#     print "Duration of stay risk/ Total trip length risk : ",stay_risk
#     return stay_risk
#
# def get_trip_type_risk(type):
#     if type == 1:
#         type_risk = risk_constants.LOW_RISK
#     elif type <= 3:
#         type_risk = risk_constants.MODERATE_RISK
#     else :
#         type_risk = risk_constants.HIGH_RISK
#     print "Trip Type Risk (Single/Maultiplt) : ",type_risk
#     return type_risk