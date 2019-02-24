import json, re
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
def send_mass_message(floor_ids, text):
	all_phone_nums = db.get_phone_nums(floor_ids)

	for next_phone_num in all_phone_nums:
		send_message(next_phone_num, text)
	#NEED TO INSERT TO TABLE OF MASS MESSAGES(HISTORY)
	db.insert_to_mass_messages(floor_ids, text, datetime.now())

#Reciever ex: '+12343423523'
def send_message(receiver, text):
	client = create_client()
	sender = keys['phone_number']
	message = client.messages.create(from_=sender, body=text, to=receiver)
	return message

def process_response(sender, text):
	if is_valid_email(text):
		db.edit_student_phone(text.lower(), sender)
	return text

def phone_to_int(str_phone_number): # convert '+12345678910' into 12345678910
	return int(str_phone_number[1:])

def phone_to_str(int_phone_number): # convert 12345678910 into '+12345678910'
	return '+'+str(int_phone_number)

def is_valid_email(email): # method to check if given email is valid format
	pattern = "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$"
	return re.match(pattern, email.strip()) != None
