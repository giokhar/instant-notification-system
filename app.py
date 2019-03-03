from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO
# custom imports
from helpers.twilio import process_response, send_mass_message, send_chat_message
from helpers.database import get_all_students, get_alert_names, get_alert_template, get_audience_names, get_last_read_student_id, get_all_chat_messages_with, get_students_recent_messages_with_unread_count, edit_unread_count
from helpers.custom import format_floor_ids, format_data_times

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

def render_template_with_dict(template, extra):
	"""Helper function to render a template using some common variables"""
	common_dict = {}
	return render_template(template, data={**common_dict, **extra})

@app.route("/")
def dashboard_page():
	data = {}
	return render_template_with_dict('dashboard.html', data)

@app.route("/students")
def student_data_page():
	data = {}
	data['students'] = get_all_students()
	return render_template_with_dict('students.html', data)

@app.route("/register-student")
def register_student_page():
	data = {}
	return render_template_with_dict('register_student.html', data)

@app.route("/mass-message", methods=['GET', 'POST'])
def mass_message_page():
	data = {}
	floor_ids_list = request.form.getlist('selected_audience')

	if request.form.get('message') and floor_ids_list:
		floor_ids = format_floor_ids(floor_ids_list)
		print(floor_ids)
		text = request.form.get('message')
		send_mass_message(floor_ids, text) 
		return redirect("/chat")
	elif request.form.get('type_id'):
		data['audience'] = get_audience_names()
		data['message_template'] = get_alert_template(request.form.get('type_id'))
		return render_template_with_dict('mass_message.html', data)
	else:
		data['message_types'] = get_alert_names()
		return render_template_with_dict('mass_message_type.html', data)

@app.route("/chat")
def chat_page():
	student_id = 1
	if get_last_read_student_id():
		student_id = get_last_read_student_id()[0]
	return redirect('/chat/'+str(student_id))

@app.route("/chat/<student_id>", methods=['GET', 'POST'])
def chat_user_page(student_id):
	data = {}
	edit_unread_count(student_id, 0) # clear unread messages when I open it
	messages_with_unread_count = get_students_recent_messages_with_unread_count() # get sidebar info
	data['students'] = format_data_times(messages_with_unread_count) # get sidebar info formated dates
	data['messages'] = get_all_chat_messages_with(student_id) # get chat history
	return render_template_with_dict('chat.html', data)

@app.route("/about")
def about_page():
	data = {}
	return render_template_with_dict('about.html', data)

@socketio.on('my_event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + str(data))
    socketio.emit('message_sent', data)
    send_chat_message(data['student_id'],data['message'])


@app.route("/listener", methods=['GET', 'POST'])
def listener():
	"""Listener method to listen to incoming messages"""
	auto_response = process_response(request, socketio)
	return str(request)

if __name__ == "__main__":
    app.run(debug=True)