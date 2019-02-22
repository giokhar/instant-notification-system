from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import helper as hlp

app = Flask(__name__)


@app.route("/")
def main():
	try:
		hlp.migration() # it will try to make migration if db does not exist
	except:
		pass
	with hlp.connect_db() as con:
		query = "select * from students"
		cur = con.cursor()
		cur.execute(query)
		rows = cur.fetchall();
		print(rows)
	return "MY APP"


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