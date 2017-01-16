import requests
import api_endpoints
import request_headers
import access_tokens


def get_user_profile_data(user_id):
    params = {
        "access_token" : access_tokens.viola_access_token
    }

    return requests.get(api_endpoints.user_profile_endpoint.format(user_id), headers = request_headers.default_header, params = params ).json()


def send_plain_text_message(user_id, message):
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": message
        }
    }

    params = {
        "access_token" : access_tokens.viola_access_token
    }

    resp = requests.post(api_endpoints.send_api_endpoint, headers = request_headers.default_header, params = params, json = data)
    if resp.json()['recipient_id'] and resp.json()['message_id']:
        pass
    else:
        pass
        #log here

def getting_started_button_click_action(message):
    sender = message['sender']['id']
    profile_data = get_user_profile_data(sender)

    response_message = "Hi, {} {}. This is Viola. Your travel insurance buddy. How may I help you ? :)".format(profile_data['first_name'], profile_data['last_name'])
    send_plain_text_message(sender, response_message)






