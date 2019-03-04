from flask import Flask, request, redirect, render_template, session
from flask_socketio import SocketIO
# custom imports
from helpers.twilio import process_response, send_mass_message, send_chat_message
from helpers.database import get_all_students, get_alert_names, get_alert_template, get_audience_names, get_last_read_student_id, get_all_chat_messages_with, get_students_recent_messages_with_unread_count, edit_unread_count, get_students_recent_messages_with_unread_messages, get_all_reports, get_todays_reports, get_all_mass_messages, format_data_floors, get_chart_data, check_user_credentials
from helpers.custom import format_floor_ids, format_data_times

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'NO_SECRET_KEY'
socketio = SocketIO(app)

def render_template_with_dict(template, extra):
	"""Helper function to render a template using some common variables"""
	common_dict = {}
	common_dict['unread_students'] = format_data_times(get_students_recent_messages_with_unread_messages())
	common_dict['today_reports'] = format_data_times(get_todays_reports(), time_index=4)
	return render_template(template, data={**common_dict, **extra})

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = "" 
	username = request.form.get('username')
	password = request.form.get('password')
	if username and password:
		if check_user_credentials(username, password) != None:
			session['username'] = username
			return redirect('/')
		error = '<div class="alert alert-danger mb-2" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><strong>Oh snap!</strong> Username or password is incorrect</div>'
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/login')

@app.route("/")
def dashboard_page():
	if 'username' in session:
		data = {}
		data['timeline']=[]
		data['report_counts']=[]
		data['non_report_counts'] = []
		data['total_reports'] = 0
		data['total_messages'] = 0
		reports = get_chart_data(1) # get all report count
		non_reports = get_chart_data(0) # get all non-report messages
		for report in reports:
			data['timeline'].append(report[0]) # append day to the timeline
			data['report_counts'].append(report[1]) # append appropriate count number
			data['total_reports'] += int(report[1])
		for non_report in non_reports:
			data['non_report_counts'].append(non_report[1]) # append appropriate count number
			data['total_messages'] += int(non_report[1])
		return render_template_with_dict('dashboard.html', data)
	return redirect('login')

@app.route("/students")
def student_data_page():
	if 'username' in session:
		data = {}
		data['students'] = get_all_students()
		return render_template_with_dict('students.html', data)

@app.route("/register-student")
def register_student_page():
	if 'username' in session:
		data = {}
		return render_template_with_dict('register_student.html', data)
	return redirect('/login')

@app.route("/mass-message", methods=['GET', 'POST'])
def mass_message_page():
	if 'username' in session:
		data = {}
		floor_ids_list = request.form.getlist('selected_audience')

		if request.form.get('message') and floor_ids_list:
			floor_ids = format_floor_ids(floor_ids_list)
			text = request.form.get('message')
			send_mass_message(floor_ids, text) 
			return redirect("/mass-history")
		elif request.form.get('type_id'):
			data['audience'] = get_audience_names()
			data['message_template'] = get_alert_template(request.form.get('type_id'))
			return render_template_with_dict('mass_message.html', data)
		else:
			data['message_types'] = get_alert_names()
			return render_template_with_dict('mass_message_type.html', data)
	return redirect('/login')

@app.route("/mass-history")
def mass_history_page():
	if 'username' in session:
		data = {}
		data['mass-messages'] = format_data_times(format_data_floors(get_all_mass_messages()), time_index=3)
		return render_template_with_dict('mass-history.html', data)
	return redirect('/login')

@app.route("/reports")
def reports_page():
	if 'username' in session:
		data = {}
		data['reports'] = format_data_times(get_all_reports(), time_index=4)
		return render_template_with_dict('reports.html', data)
	return redirect('/login')

@app.route("/chat")
def chat_page():
	if 'username' in session:
		student_id = 1
		if get_last_read_student_id():
			student_id = get_last_read_student_id()[0]
		return redirect('/chat/'+str(student_id))
	return redirect('/login')

@app.route("/chat/<student_id>", methods=['GET', 'POST'])
def chat_user_page(student_id):
	if 'username' in session:
		data = {}
		edit_unread_count(student_id, 0) # clear unread messages when I open it
		messages_with_unread_count = get_students_recent_messages_with_unread_count() # get sidebar info
		data['students'] = format_data_times(messages_with_unread_count) # get sidebar info formated dates
		data['messages'] = get_all_chat_messages_with(student_id) # get chat history
		return render_template_with_dict('chat.html', data)
	return redirect('/login')

@app.route("/about")
def about_page():
	if 'username' in session:
		data = {}
		return render_template_with_dict('about.html', data)
	return redirect('/login')

@socketio.on('my_event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    # print('received my event: ' + str(data))
    socketio.emit('message_sent', data)
    send_chat_message(data['student_id'],data['message'])

@app.route("/listener", methods=['GET', 'POST'])
def listener():
	"""Listener method to listen to incoming messages"""
	auto_response = process_response(request, socketio)
	return str(request)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app)