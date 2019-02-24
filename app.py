from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import Message, MessagingResponse
# custom imports
from helpers.twilio import process_response
from helpers.database import get_all_students, get_alert_names, get_alert_template, get_audience_names

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def dashboard_page():
	return render_template('dashboard.html')

@app.route("/students")
def student_data_page():
	students = get_all_students()
	return render_template('students.html', students=students)

@app.route("/register-student")
def register_student_page():
	return render_template('register_student.html')

@app.route("/mass-message", methods=['GET', 'POST'])
def mass_message_page():
	if request.form.get('type_id'):
		audience = get_audience_names()
		message_template = get_alert_template(request.form.get('type_id'))
		return render_template('mass_message.html', message_template=message_template, audience=audience)
	else:
		message_types = get_alert_names()
		return render_template('mass_message_type.html', message_types=message_types)

@app.route("/chat")
def chat_page():
	return render_template('chat.html')

@app.route("/about")
def about_page():
	return render_template('about.html')


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