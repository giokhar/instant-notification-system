from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import helper as hlp

app = Flask(__name__)

@app.route("/")
def main():
	with hlp.connection.cursor() as cursor:
		cursor.execute("SELECT * FROM halls")

		result = cursor.fetchall()

	print(result)
	return "My App"


@app.route("/listener", methods=['GET', 'POST'])
def listener():
	"""Listener method to listen to incoming messages"""
	resp = MessagingResponse()
	text = request.values['Body'] # get message text from request.values 
	sender = request.values['From'] # get sender phone number in the format '+12345678910'

	auto_response = hlp.process_response(sender, text) # get the response from helper function
	#resp.message(auto_response) # respond to sender with the message from processResponse method

	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)