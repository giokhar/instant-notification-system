import json, pymysql

# Get Configuration file keys.json and store values in the variable 'keys'
try:keys = json.loads(open('helpers/keys.json').read())
except:raise FileNotFoundError("Configuration file keys.json not found, contact the owner to get access!")

connection = pymysql.connect(keys['db_host'],keys['db_user'],keys['db_pass'],keys['db_name'])


# ALL CUSTOM METHODS TO PULL DATA FROM DATABASE GOES HERE

#If the tuples in the table contain one element,
#this method converts the table into a list and returns that list.
def format_sql_result(lst):
	result = []
	for next in lst:
		result.append(next[0])
	return result

#Is given a string containing floor_ids and returns a list of 
#phone numbers(strings, ex : '+123213124') of students living on those floors.
def get_phone_nums(floor_ids):
	floor_ids = floor_ids.split(',')

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * len(floor_ids)) #format the floor_ids so it fils sql query
		print(format_strings)
		cursor.execute("SELECT phone FROM students where floor_id IN (%s)" % format_strings, tuple(floor_ids))
		result = cursor.fetchall()

	result = format_sql_result(result)
	return result

#Returns a table(tuple of tuples) of all students(fn,ln,email,phone) with their hall and floor names.
def get_all_students():
	with connection.cursor() as cursor:
		cursor.execute("SELECT students.first, students.last, students.email, halls.name, floors.name, students.phone FROM students INNER JOIN floors ON students.floor_id=floors.id INNER JOIN halls ON halls.id=floors.hall_id")
		result = cursor.fetchall()
	return result

#Given the type_id of the alert
#returns the template message for given type_id.
def get_alert_template(type_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT template FROM alerts WHERE type_id=%s", (type_id,))
		template = cursor.fetchone()[0] #This returns a tuple and we pick the first element.

	return template

#Givent the student_id returns the phone number of this student.
def get_student_phone(student_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT phone FROM students WHERE id=%s", (student_id,))
		phone = cursor.fetchone()[0] #This returns a tuple and we pick the first element.

	return phone

#all given values are strings
#Updates the data of a student with a given id.
def edit_student(id, first, last, email, floor_id, phone):
	with connection.cursor() as cursor:
		args = (first, last, email, floor_id, phone, id) #a tuple of arguments
		cursor.execute("UPDATE students SET first=%s, last=%s, email=%s, floor_id=%s, phone=%s WHERE id=%s",args)

		connection.commit()
#Edits the phone number of the student with a given email address.
def edit_student_phone(email, phone):
	with connection.cursor() as cursor:
		args = (phone, email)
		cursor.execute("UPDATE students SET phone=%s WHERE email=%s", args)

		connection.commit()

#Each argument is given as a string.
#Adds a new student into the database.
def register_student(first, last, email, floor_id, phone):
	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * 5) #argc == 5

		cursor.execute("INSERT INTO students (first, last, email, floor_id, phone) VALUES (%s)" % format_strings, (first, last, email, floor_id, phone))

		connection.commit()

#Inserts the old messages to the mass_messages table.
def insert_to_mass_messages(floor_ids, message, time):
	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * 3) #argc == 5

		cursor.execute("INSERT INTO mass_messages (floor_ids, message, time) VALUES (%s)" % format_strings, (floor_ids, message, time))

		connection.commit()
#Inserts the old messages sent in the chat into the chat_messages table.
def insert_to_chat_messages(student_id, message, time, is_sender):
	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * 4) #argc == 5

		cursor.execute("INSERT INTO chat_messages (student_id, message, time, is_sender) VALUES (%s)" % format_strings, (student_id, message, time, is_sender))

		connection.commit()

