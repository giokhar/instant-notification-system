from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import Message, MessagingResponse
# custom imports
from helpers.twilio import process_response
from helpers.database import connection

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def dashboard_page():
	return render_template('dashboard.html')

@app.route("/students")
def student_data_page():
	return render_template('dashboard.html')

@app.route("/students/register")
def register_student_page():
	return render_template('dashboard.html')

@app.route("/mass-message"):
def mass_message_page():
	return render_template('dashboard.html')

@app.route("/chat")
def chat_page():
	return render_template('dashboard.html')

@app.route("/about")
def about_page():
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