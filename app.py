import json
from twilio.rest import Client

keys = json.loads(open('keys.json').read())
account_sid = keys['account_sid']
auth_token = keys['auth_token']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hi how are you?",
                     from_=keys['phone_number'],
                     to='+17654070369'
                 )

print(message.sid)