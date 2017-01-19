import risk_constants


def get_risk_by_marital_status(status):
    risk = risk_constants.LOW_RISK if status.lower() == "married" else risk_constants.MODERATE_RISK
    print('STATUS : Risk for marital status as {} - {}'.format(status, risk_constants.risk_status[risk]))
    return risk


def get_risk_by_age(age):
    if age < 17:
        risk = risk_constants.NO_RISK
    elif age < 35:
        risk = risk_constants.LOW_RISK
    elif age < 60:
        risk = risk_constants.MODERATE_RISK
    elif age < 90:
        risk = risk_constants.HIGH_RISK
    else:
        risk = risk_constants.EXTREME_RISK

    print('STATUS : Age risk for age {} - {}'.format(age, risk_constants.risk_status[risk]))
    return risk