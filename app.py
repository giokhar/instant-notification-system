from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO
# custom imports
from helpers.twilio import process_response, send_mass_message
from helpers.database import get_all_students, get_alert_names, get_alert_template, get_audience_names, get_last_read_student_id, get_all_chat_messages_with, get_students_recent_messages_with_unread_count
from helpers.custom import format_floor_ids

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
	floor_ids_list = request.form.getlist('selected_audience')

	if request.form.get('message') and floor_ids_list:
		floor_ids = format_floor_ids(floor_ids_list)
		print(floor_ids)
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
	student_id = get_last_read_student_id()
	return redirect('/chat/'+str(student_id))

@app.route("/chat/<student_id>", methods=['GET', 'POST'])
def chat_user_page(student_id):
	students = get_students_recent_messages_with_unread_count()
	messages = get_all_chat_messages_with(student_id)
	return render_template('chat.html', messages=messages, students=students)

@app.route("/about")
def about_page():
	return render_template('about.html')

@socketio.on('my_event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + str(data))
    socketio.emit('message_sent', data)


@app.route("/listener", methods=['GET', 'POST'])
def listener():
	"""Listener method to listen to incoming messages"""
	auto_response = process_response(request)
	return str(request)

if __name__ == "__main__":
    app.run(debug=True)