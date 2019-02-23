from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import Message, MessagingResponse
# custom imports
from helpers.twilio import process_response
from helpers.database import connection

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def main():
	
	return render_template('dashboard.html')


@app.route("/listener", methods=['GET', 'POST'])
def listener():
	"""Listener method to listen to incoming messages"""
	resp = MessagingResponse()
	text = request.values['Body'] # get message text from request.values 
	sender = request.values['From'] # get sender phone number in the format '+12345678910'

	auto_response = process_response(sender, text) # get the response from helpers.twilio.process_response
	#resp.message(auto_response) # respond to sender with the automatic response

	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)