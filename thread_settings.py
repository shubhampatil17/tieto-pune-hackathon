import requests
import request_headers
import api_endpoints
import access_tokens


def set_getting_started_button():
    data = {
        "setting_type": "call_to_actions",
        "thread_state": "new_thread",
        "call_to_actions": '[{"payload": "PAYLOAD_FOR_GETTING_STARTED_BUTTON"}]'
    }

    params = {
        "access_token" : access_tokens.viola_access_token
    }

    resp = requests.post(api_endpoints.thread_setting_endpoint, json = data, params = params, headers = request_headers.default_header)
    if resp.json()['result']:
        print "Getting started button set successfully"
    else:
        print "Error : Getting started button"
        #log here


def set_greeting_text():
    data = {
        "setting_type": "greeting",
        "greeting": {
            "text": unicode("VIOLA : Virtual Insurance Optimisation Learning Agent", "utf-8")
        }
    }

    params = {
        "access_token" : access_tokens.viola_access_token
    }

    resp = requests.post(api_endpoints.thread_setting_endpoint, json = data, params = params, headers = request_headers.default_header)
    print "Greeting text set successfully"


def setup_bot_thread():
    set_greeting_text()
    set_getting_started_button()