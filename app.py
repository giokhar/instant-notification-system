# import json
# from twilio.rest import Client
from flask import Flask, request, redirect
from twilio import twiml

app = Flask(__name__)

# @app.route("/sms", methods=['GET', 'POST'])
# def sms_ahoy_reply():
#     """Respond to incoming messages with a friendly SMS."""
#     # Start our response
#     resp = twiml.Response()

#     # Add a message
#     resp.message("Ahoy! Thanks so much for your message.")

#     return str(resp)

@app.route("/", methods=["GET"])
def main():
	return "Giorgi is the best software engineer"

if __name__ == "__main__":
    app.run(debug=True)

# keys = json.loads(open('keys.json').read())
# account_sid = keys['account_sid']
# auth_token = keys['auth_token']
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                      body="Hi how are you?",
#                      from_=keys['phone_number'],
#                      to='+17654070369'
#                  )

# print(message.sid)