import requests
import json
import os
#from firebase_admin import initialize_app
#from firebase_admin import messaging

""""
app = initialize_app()
mytoken = "some_token"
noti = messaging.Notification(title="Hola", body="quetal")
msg = messaging.Message(data={'fooo': 'baar'}, token=mytoken, notification=noti)
messaging.send(msg)
"""

auth = os.environ.get('FIREBASE_AUTH')

headers = {
    'Authorization': f'key={auth}',
    'Content-Type': 'application/json',
}


def send_message_to(token, title, mensaje, data, to_delivery=False):

    post_data = {
        "to": token,
        "notification": {
            "android": {"priority": "high"},
            "title": title,
            "body": mensaje,
            "click_action": "open_client_chat"
        },
        "data": data
    }

    post_data['notification']['click_action'] = 'open_delivery_chat' if to_delivery else 'open_client_chat'
    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(post_data))

    if response.status_code == 200:
        return 'OK'
    else:
        return response.text