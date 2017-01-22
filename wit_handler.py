from wit import Wit
import access_tokens
from premium_calculator import calculate_premium_for_trip
import facebook_custom_actions
import facebook_custom_actions
from main import session
import copy

def check_insurance_type_validity(request):
    context = request['context']
    entities = request['entities']

    if 'insuranceType' not in entities:
        context['missing_insurance_type'] = True
    else:
        context = {}

        if not entities['insuranceType'][0]['value'].lower() == 'travel':
            context['invalid_insurance_type'] = True
        else:
            context['valid_insurance_type'] = True

    return context


def add_trip_plan(request):
    context = request['context']
    entities = request['entities']

    # print(entities)

    if 'trip_schedule' not in context:
        context['trip_schedule'] = []

    if 'location' in entities:
        context['current_destination'] = entities['location'][0]['value'].lower()

    if 'datetime' in entities:
        context['current_start_date'] = entities['datetime'][0]['value'].split('.')[0]

    if 'current_destination' in context and 'current_start_date' in context:
        if 'missing_location' in context:
            del context['missing_location']

        if 'missing_date' in context:
            del context['missing_date']

        context['valid_trip_plan'] = True
        context['trip_schedule'].append({
            'destination': context['current_destination'],
            'start_date': context['current_start_date']
        })

        del context['current_destination']
        del context['current_start_date']

    elif 'current_destination' not in context:
        if 'valid_trip_plan' in context:
            del context['valid_trip_plan']

        if 'missing_date' in context:
            del context['missing_date']

        context['missing_location'] = True

    elif 'current_start_date' not in context:
        if 'valid_trip_plan' in context:
            del context['valid_trip_plan']

        if 'missing_location' in context:
            del context['missing_location']

        context['missing_date'] = True

    # print(context)
    return context


def add_return_date_to_plan(request):
    context = request['context']
    entities = request['entities']
    # print(entities)

    if 'datetime' in entities:
        return_date = entities['datetime'][0]['value'].split('.')[0]
        context['trip_schedule'].append({
            'start_date' : return_date
        })

    # print(context)
    return context


def add_age_to_plan(request):
    context = request['context']
    entities = request['entities']
    # print(entities)

    if 'age' in entities:
        age = entities['age'][0]['value']
        context['age'] = int(age.replace('years', ''))

    # print(context)
    return context


def add_marital_status_to_plan(request):
    context = request['context']
    entities = request['entities']
    # print(entities)

    if 'maritalStatus' in entities:
        marital_status = entities['maritalStatus'][0]['value']
        context['marital_status'] = marital_status

    # print(context)
    return context


def add_trip_cost_to_plan(request):
    context = request['context']
    entities = request['entities']
    # print(entities)

    if 'amount_of_money' in entities:
        trip_cost = entities['amount_of_money'][0]['value']
        context['trip_cost'] = trip_cost

    # print(context)
    return context


def calculate_premium(request):
    context = request['context']
    trip_plan = {
        'trip_schedule': copy.deepcopy(context['trip_schedule']),
        'age': context['age'],
        'marital_status': context['marital_status'],
        'trip_cost': context['trip_cost']
    }

    premium_amount = calculate_premium_for_trip(trip_plan)
    context['premium_amount'] = premium_amount
    return context


def send(request, response):
    print(response['text'])


wit_actions = {
    'send' : send,
    'check_insurance_type_validity': check_insurance_type_validity,
    'add_trip_plan': add_trip_plan,
    'add_return_date_to_plan': add_return_date_to_plan,
    'add_age_to_plan': add_age_to_plan,
    'add_marital_status_to_plan': add_marital_status_to_plan,
    'add_trip_cost_to_plan': add_trip_cost_to_plan,
    'calculate_premium': calculate_premium
}

wit_client = Wit(access_token=access_tokens.wit_access_token, actions=wit_actions)

# def handle(session_id, message, context):
#     resp = wit_client.converse(session_id, message['message']['text'], context)
#     while not resp['type'] == 'stop':
#
#         if resp['type'] == 'msg':
#             facebook_custom_actions.send_plain_text_message(message['sender']['id'], resp['msg'])
#         elif resp['type'] == 'action':
#             entities = resp['entities'] if 'entities' in resp else None
#             context = wit_actions[resp['action']](context, entities)
#         elif resp['type'] == 'merge':
#             pass
#         else:
#             pass
#
#         resp = wit_client.converse(session_id, None, context)
#
#     return context

