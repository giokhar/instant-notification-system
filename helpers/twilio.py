import json, re, requests, os
from twilio.rest import Client
import helpers.database as db
from datetime import datetime

# Get Configuration file keys.json and store values in the variable 'keys'
try:keys = json.loads(open('helpers/keys.json').read())
except: keys = os.environ
print(keys)
def create_client():
	account_sid = keys['account_sid']
	auth_token = keys['auth_token']
	return Client(account_sid, auth_token)

#sends the message to everybody who live
#in specific floors(given by floor_ids(string)).
#Updates the database accordingly.
def send_mass_message(floor_ids, text):
	all_phone_nums = db.get_phone_nums(floor_ids)

	for next_phone_num in all_phone_nums:
		send_message(next_phone_num, text)
	# Inserts into mass_messages table to keep track of all the messages
	db.insert_to_mass_messages(floor_ids, text, datetime.now())

#Sends a chat message.
#Updates the database accordingly.
def send_chat_message(student_id, text):
	receiver = db.get_student_phone(student_id)
	send_message(receiver, text)
	db.insert_to_chat_messages(student_id, text, datetime.now(), False, False, False)

#Reciever ex: '+12343423523'
def send_message(receiver, text):
	client = create_client()
	sender = keys['phone_number']
	message = client.messages.create(from_=sender, body=text, to=receiver)
	return message

def process_image(request, filename, student_id):
	text = "downloads/"+filename
	with open('{}/{}'.format(keys['download_url'], filename), 'wb') as f:
		image_url = request.values['MediaUrl0']
		f.write(requests.get(image_url).content)
	db.insert_to_chat_messages(student_id, text, datetime.now(), True, False, True) # insert image url into chat_messages table
	return text

def process_response(request, socketio):
	if request.values.get('NumMedia', False):
		phone = request.values['From']
		text = request.values['Body'].strip()

		try:
			# Check if user phone number exists and then let them add the image
			student_id = db.get_student_id(phone) #Throws an error if such student doesn't exist.


			#if this student has never sent a message before
			if not db.get_all_chat_messages_with(student_id):
				send_message(phone, "Hello, You can report or talk to public safety.\nYour report should be in the following format: \n$MY REPORT")
			#_____________________________________
			
			#DEFAULT
			is_report = False
			is_sender = True
			is_img = (request.values['NumMedia'] != '0')

			if text != "":
				if text[0] == "$":
					is_report = True
					text=text[1:]
					send_message(phone, "Thank you for your report!")

			if is_img: #processing the images sent via text message.
				filename = request.values['MessageSid']+'.png'
				text = "downloads/"+filename
				process_image(request, filename, student_id) # download image first
				socketio.emit('message_received', {"student_id":student_id, "message":text, "name":db.get_student_name(student_id), "is_img":is_img, "is_report":is_report}) # then emit the socket
				socketio.emit('add_message_to_header', {"student_id":student_id, "message":"Image", "name":db.get_student_name(student_id) }) # add message to the header panel
			elif is_report: # processing reports
				socketio.emit('message_received', {"student_id":student_id, "message":text, "name":db.get_student_name(student_id), "is_img":is_img, "is_report":is_report}) # when regular text message is sent
				socketio.emit('add_report_to_header', {"student_id":student_id, "message":text, "name":db.get_student_name(student_id)})
				db.insert_to_chat_messages(student_id, text, datetime.now(), is_sender, is_report, is_img)
				db.edit_unread_count(student_id, opr=1)
			else:
				socketio.emit('message_received', {"student_id":student_id, "message":text, "name":db.get_student_name(student_id), "is_img":is_img, "is_report":is_report}) # when regular text message is sent
				socketio.emit('add_message_to_header', {"student_id":student_id, "message":text, "name":db.get_student_name(student_id)})
				db.insert_to_chat_messages(student_id, text, datetime.now(), is_sender, is_report, is_img)
				db.edit_unread_count(student_id, opr=1)
		except:
			# In this case, user sent something but this phone number does not exist in the database
			# ASK USER TO REGISTER
			if is_valid_email(text):
				db.edit_student_phone(text.lower(), phone)
				send_message(phone, "Your phone number was successfully added to our database!")
			else:
				send_message(phone, "Your phone number is not in our database. Please reply with your valid email in order to register.")
	return 1
# method to check if given email is valid format
# and check if such email is in our database
def is_valid_email(email): 
	pattern = "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$"
	email = email.strip()
	return re.match(pattern, email) != None and db.if_email_exists(email)
