import json, pymysql

connection = None
#Is run in every function in this file,
#to avoid the connection timeout 
def restart_connection():
	global connection

	if connection != None and connection.open:
		connection.close()
	# Get Configuration file keys.json and store values in the variable 'keys'
	try:keys = json.loads(open('helpers/keys.json').read())
	except:raise FileNotFoundError("Configuration file keys.json not found, contact the owner to get access!")
	#changing the global variable connection.
	connection = pymysql.connect(keys['db_host'],keys['db_user'],keys['db_pass'],keys['db_name'])

#HELPER FUNCTION
#If the tuples in the table contain one element,
#this method converts the table into a list and returns that list.
def format_sql_result(lst):
	result = []
	for next in lst:
		result.append(next[0])
	return result

#GET FUNCTIONS
#Is given a string containing floor_ids and returns a list of 
#phone numbers(strings, ex : '+123213124') of students living on those floors.
def get_phone_nums(floor_ids):
	restart_connection()

	floor_ids = floor_ids.split('.')

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * len(floor_ids)) #format the floor_ids so it fits sql query
		cursor.execute("SELECT phone FROM students WHERE floor_id IN (%s)" % format_strings, tuple(floor_ids))
		result = cursor.fetchall()

	result = format_sql_result(result)
	return result

#Returns a table(tuple of tuples) of all students(fn,ln,email,phone) with their hall and floor names.
def get_all_students():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT students.first, students.last, students.email, halls.name, floors.name, students.phone FROM students INNER JOIN floors ON students.floor_id=floors.id INNER JOIN halls ON halls.id=floors.hall_id")
		result = cursor.fetchall()
	return result

#Given the type_id of the alert
#returns the template message for given type_id.
def get_alert_template(type_id):
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT template FROM alerts WHERE type_id=%s", (type_id,))
		template = cursor.fetchone()[0] #This returns a tuple and we pick the first element.

	return template

# Returns types and names for all alerts
def get_alert_names():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT type_id, name FROM alerts ORDER BY type_id")
		result = cursor.fetchall()
	return result

#Returns a list of [(aud, halls.name, [(floors.id, floor.name),...]),...] 
def get_audience_names():
	restart_connection()

	list_audience = []
	list_halls = get_hall_names()
	for next_hall in list_halls:
		aud = next_hall[0]
		hall_name = next_hall[1]
		floors = get_floor_names(next_hall[2])
		list_audience.append((aud, hall_name, floors))

	return list_audience

#Returns a list of halls grouped by concatinated floor_ids(string)
def get_hall_names():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT GROUP_CONCAT(floors.id SEPARATOR '.') as aud, halls.name, halls.id FROM floors INNER JOIN halls ON halls.id = floors.hall_id GROUP BY halls.name")
		result = cursor.fetchall()

	return result

#Returns a list of (id, name) of floors based on hall_id(int)
def get_floor_names(hall_id):
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT id, name FROM floors WHERE hall_id=%s ORDER BY id", (hall_id,))
		result = cursor.fetchall()
	return result

#Floor_ids format: string containing dot separated values
#Based on the floor_ids it returns a list containing
#the tuples of (hall name, floor name)
def get_floor_names_by_floor_ids(floor_ids):
	restart_connection()
	
	floor_ids = floor_ids.split('.')

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * len(floor_ids))

		cursor.execute("SELECT halls.name, floors.name FROM floors INNER JOIN halls ON floors.hall_id=halls.id WHERE floors.id IN (%s)" % format_strings, tuple(floor_ids))
		result = cursor.fetchall()

	return result

#Given the student_id returns the phone number of this student.
def get_student_phone(student_id):
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT phone FROM students WHERE id=%s", (student_id,))
		phone = cursor.fetchone()[0] #This returns a tuple and we pick the first element.

	return phone

#Given the phone number returns the id of this student.
#Gives error when such student doesn't exist
def get_student_id(phone):
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT id FROM students WHERE phone=%s", (phone,))
		phone = cursor.fetchone()[0] #This returns a tuple and we pick the first element.

	return phone


#returns a list of tuples containing message, is_sender,time  associated with a given student_id.
#Format: [(student_id, message, is_sender, time)]
def get_all_chat_messages_with(student_id):
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT student_id, message, is_sender, is_img, time FROM chat_messages WHERE student_id=%s ORDER BY time ASC", (student_id,))
		result = cursor.fetchall()
	return result

#Returns the entries id, floor_ids, message and time
#from the mass messages table.
#Format: list of tuples
def get_all_mass_messages():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM mass_messages ORDER BY time ASC")
		result = cursor.fetchall()

	return result

#returns the id of the student 
#with the most recent read message. 
def get_last_read_student_id():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT chats.student_id FROM chat_messages INNER JOIN chats ON chat_messages.student_id=chats.student_id WHERE chat_messages.is_sender=1 AND chats.unread_count=0 ORDER BY chat_messages.time DESC")
		result = cursor.fetchone()[0]
	return result

#returns all the student info with the most
#recent message and unread count
def get_students_recent_messages_with_unread_count():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT CONVERT(chats.student_id, CHAR), students.first, students.last, message, is_sender, is_report, is_img, chats.unread_count, time FROM chat_messages INNER JOIN chats ON chat_messages.student_id=chats.student_id INNER JOIN students ON chats.student_id=students.id WHERE chat_messages.id IN (SELECT MAX(chat_messages.id) FROM chat_messages GROUP BY student_id) ORDER BY time DESC")
		result = cursor.fetchall()
	return result

#uses get_students_recent_messages_with_unread_count() and
#returns the table entries where undread_count is not 0.(there are some unread messages)
def get_students_recent_messages_with_unread_messages():
	table = get_students_recent_messages_with_unread_count()
	result = []
	unread_count_index = 7 #MAGIC NUM but needed
	for next_tuple in table:
		if next_tuple[unread_count_index] != 0:
			result.append(next_tuple)
	return result 

print(get_students_recent_messages_with_unread_messages())
#student name, last name, message, sorted by time
def get_all_reports():
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT students.first, students.last, chat_messages.message, chat_messages.time FROM students INNER JOIN chat_messages ON students.id=chat_messages.student_id WHERE chat_messages.is_report=1 ORDER BY time DESC")
		result = cursor.fetchall()
	return result

#all given values are strings
#Updates the data of a student with a given id.
def edit_student(id, first, last, email, floor_id, phone):
	restart_connection()

	with connection.cursor() as cursor:
		args = (first, last, email, floor_id, phone, id) #a tuple of arguments
		cursor.execute("UPDATE students SET first=%s, last=%s, email=%s, floor_id=%s, phone=%s WHERE id=%s",args)

		connection.commit()

#Given a student_id and opr(operation type-> 0 - sets unread_count to 0, 1 - increments unread_count by1)
#updates the unread_count from the table chats accordingly.
def edit_unread_count(student_id, opr):
	restart_connection()

	with connection.cursor() as cursor:
		if (opr == 0):
			cursor.execute("UPDATE chats SET unread_count=0 WHERE student_id=%s", (student_id,))
		else:
			cursor.execute("UPDATE chats SET unread_count=unread_count+1 WHERE student_id=%s", (student_id,))
		connection.commit()

#Updates the phone number of the student with a given email address.
def edit_student_phone(email, phone):
	restart_connection()

	with connection.cursor() as cursor:
		args = (phone, email)
		cursor.execute("UPDATE students SET phone=%s WHERE email=%s", args)

		connection.commit()

#Each argument is given as a string.
#Adds a new student into the database.
def register_student(first, last, email, floor_id, phone):
	restart_connection()

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * 5) #argc == 5

		cursor.execute("INSERT INTO students (first, last, email, floor_id, phone) VALUES (%s)" % format_strings, (first, last, email, floor_id, phone))

		connection.commit()

#Inserts the old messages to the mass_messages table.
def insert_to_mass_messages(floor_ids, message, time):
	restart_connection()

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * 3) #argc == 5

		cursor.execute("INSERT INTO mass_messages (floor_ids, message, time) VALUES (%s)" % format_strings, (floor_ids, message, time))

		connection.commit()
#Inserts the old messages sent in the chat into the chat_messages table.
def insert_to_chat_messages(student_id, message, time, is_sender, is_report, is_img):
	restart_connection()

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * 6) #argc == 5

		cursor.execute("INSERT INTO chat_messages (student_id, message, time, is_sender, is_report, is_img) VALUES (%s)" % format_strings, (student_id, message, time, is_sender, is_report, is_img))

		connection.commit()

#With a given email checks if such email exists in the database 
#and returns a corresponding boolean value.
def if_email_exists(email):
	restart_connection()

	with connection.cursor() as cursor:
		cursor.execute("SELECT id FROM students WHERE email=%s", (email,))
		result = cursor.fetchall()
	return len(result) != 0