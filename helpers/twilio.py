import json, re, requests
from twilio.rest import Client
import helpers.database as db
from datetime import datetime

# Get Configuration file keys.json and store values in the variable 'keys'
try:keys = json.loads(open('helpers/keys.json').read())
except:raise FileNotFoundError("Configuration file keys.json not found, contact the owner to get access!")

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
	db.insert_to_chat_messages(student_id, text, datetime.now(), True, False, False)

#Reciever ex: '+12343423523'
def send_message(receiver, text):
	client = create_client()
	sender = keys['phone_number']
	message = client.messages.create(from_=sender, body=text, to=receiver)
	return message

def process_response(request):
	if request.values.get('NumMedia', False):
		phone = request.values['From']
		text = request.values['Body']
		try:
			# Check if user phone number exists and then let them add the image
			student_id = db.get_student_id(phone)
			if request.values['NumMedia'] != '0':
				filename = request.values['MessageSid']+'.png'
				text = keys['static']+"/"+filename
				with open('{}/{}'.format(keys['download_url'], filename), 'wb') as f:
					image_url = request.values['MediaUrl0']
					f.write(requests.get(image_url).content)
				db.insert_to_chat_messages(student_id, text, datetime.now(), True, False, True) # insert image url into chat_messages table
				send_message(phone, "Thanks for the image!")
			else:
				# This is the case when user sends just a text message and their phone number is registered in the database
				pass
		except:
			# In this case, user sent something but this phone number does not exist in the database
			# ASK USER TO REGISTER WITH SEVERAL PROMPTS
			if is_valid_email(text):
				db.add_student_phone(text.lower(), phone)
	else:
		print("Waiting for the request")
	return 1

def is_valid_email(email): # method to check if given email is valid format
	pattern = "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$"
	return re.match(pattern, email.strip()) != None
