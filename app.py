from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO
# custom imports
from helpers.twilio import process_response, send_mass_message
from helpers.database import keys, get_all_students, get_alert_names, get_alert_template, get_audience_names

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

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
	if request.form.get('message') and request.form.getlist('selected_audience'):
		floor_ids = ",".join(request.form.getlist('selected_audience'))
		text = request.form.get('message')
		send_mass_message(floor_ids, text) 
		return redirect("/chat")
	elif request.form.get('type_id'):
		audience = get_audience_names()
		message_template = get_alert_template(request.form.get('type_id'))
		return render_template('mass_message.html', message_template=message_template, audience=audience)
	else:
		message_types = get_alert_names()
		return render_template('mass_message_type.html', message_types=message_types)

@app.route("/chat")
def chat_page():
	# GET THE MOST RECENT USER ID BASED ON LAST MESSAGE
	user_id = 1
	return redirect('/chat/'+str(user_id))

@app.route("/chat/<user_id>")
def chat_user_page(user_id):
	print(user_id)
	return render_template('chat.html')

@app.route("/about")
def about_page():
	return render_template('about.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json)


@app.route("/listener", methods=['GET', 'POST'])
def listener():
	"""Listener method to listen to incoming messages"""
	auto_response = process_response(request)

	return str(request)

if __name__ == "__main__":
    app.run(debug=True)