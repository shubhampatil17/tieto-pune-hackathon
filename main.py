from flask import Flask, request, session
from datetime import datetime

import payload_action
import wit_handler
import uuid

app = Flask(__name__)
context = {}

@app.route('/eventWebhook')
def verify_webhook():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == 'my_verification_token':
        res, status = request.args.get('hub.challenge'), 200
    else:
        res, status = 'Random Error', 403

    return res, status

@app.route('/eventWebhook', methods=['POST'])
def get_event_webhook_data():
    global context
    event_data = request.get_json(force=True)

    if 'timestamp' in session and (datetime.now() - session['timestamp']).days > 7:
        session.clear()
        context = {}

    if 'timestamp' not in session:
        session['id'] = str(uuid.uuid4())
        session['timestamp'] = datetime.now()

    if 'entry' in event_data:
        for entry in event_data['entry']:
            if 'messaging' in entry:
                for message in entry['messaging']:
                    context['user_id'] = message['sender']['id']

                    if 'postback' in message:
                        payload_action.action_for_payload[message['postback']['payload']](message)
                    elif 'message' in message:
                        context = wit_handler.handle(session['id'], message, context)
                    else:
                        pass


    return "OK", 200


