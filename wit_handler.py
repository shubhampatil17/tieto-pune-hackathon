from wit import Wit
import access_tokens
import facebook_custom_actions
import person_details
import premium_calculator
import facebook_custom_actions
from main import session

def check_insurance_type_validity(context, entities):
    if entities:
        if 'insuranceType' not in entities:
            context['missingInsuranceType'] = True
        else:
            if 'missingInsuranceType' in context:
                del context['missingInsuranceType']

            if not entities['insuranceType'][0]['value'].lower() == 'travel':
                context['insuranceValidity'] = 'invalid'
                facebook_custom_actions.send_plain_text_message(context['user_id'], "Sorry ! I can't help with that. I am a travel insurance bot")
            else:
                context['insuranceValidity'] = 'valid'
                facebook_custom_actions.send_plain_text_message(context['user_id'], "Sure ! Please tell me about your trip plans. I want to know on which date where are you going to be presented during your trip.")

    return context


def add_trip_details(context, entities):
    if 'tripPlan' not in context:
        context['tripPlan'] = {}

    if 'location' in entities:
        context['currentLocation'] = entities['location'][0]['value']

    if 'datetime' in entities:
        context['tripPlan'][context['currentLocation']] = entities['datetime'][0]['value']
        context['validDate'] = True

        if 'missingDate' in context:
            del context['missingDate']
    else:
        context['tripPlan'][context['currentLocation']] = None
        context['missingDate'] = True

        if 'validDate' in context:
            del context['validDate']

    return context

def add_missing_date_to_trip(context, entities):

    if 'datetime' in entities:
        context['tripPlan'][context['currentLocation']] = entities['datetime'][0]['value']
        context['validDate'] = True

        if 'missingDate' in context:
            del context['missingDate']

    return context


def get_customised_premium(context, entities):

    # data = {
    #     'tripPlan' : context['tripPlan'],
    #     'age' : context['age'],
    #     'marital_status' : context['marital_status'],
    #     'Total_Cost_of_Trip' : context['total_cost_of_trip']
    # }

    #mocked for now // chat bot now yet fully functional
    data = {
        'tripPlan' : {
            u'Wellingborough' : '2017-01-10T00:00:00.000-08:00',
            u'Welwyn Garden City' : '2017-01-11T00:00:00.000-08:00',
            u'Weston-super-Mare' : '2017-01-12T00:00:00.000-08:00',
            u'Royal Tunbridge Wells' : '2017-01-13T00:00:00.000-08:00',
        },

        'age' : '20',
        'marital_status' : 'single',
        'Total_Cost_of_Trip' : '9999'
    }

    factored_data = person_details.format(data)
    premium = premium_calculator.premium_calculator(factored_data)
    facebook_custom_actions.send_plain_text_message(context['user_id'], "Your customized premium : " + str(premium))
    return context

def send(request, response):
    return request['context']


wit_actions = {
    'send' : send,
    'check_insurance_type_validity' : check_insurance_type_validity,
    'add_trip_details' : add_trip_details,
    'add_missing_date_to_trip' : add_missing_date_to_trip,
    'get_customised_premium' : get_customised_premium
}

wit_client = Wit(access_token=access_tokens.wit_access_token, actions=wit_actions)

def handle(session_id, message, context):
    resp = wit_client.converse(session_id, message['message']['text'], context)
    while not resp['type'] == 'stop':

        if resp['type'] == 'msg':
            facebook_custom_actions.send_plain_text_message(message['sender']['id'], resp['msg'])
        elif resp['type'] == 'action':
            entities = resp['entities'] if 'entities' in resp else None
            context = wit_actions[resp['action']](context, entities)
        elif resp['type'] == 'merge':
            pass
        else:
            pass

        resp = wit_client.converse(session_id, None, context)

    return context

