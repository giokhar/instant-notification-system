import json, re
from twilio.rest import Client
import helpers.database as db

# Get Configuration file keys.json and store values in the variable 'keys'
try:keys = json.loads(open('helpers/keys.json').read())
except:raise FileNotFoundError("Configuration file keys.json not found, contact the owner to get access!")

def create_client():
	account_sid = keys['account_sid']
	auth_token = keys['auth_token']
	return Client(account_sid, auth_token)

#Reciever ex: '+12343423523'
def send_message(receiver, text):
	client = create_client()
	sender = keys['phone_number']
	message = client.messages.create(from_=sender, body=text, to=receiver)
	return message

def process_response(sender, text):
	if is_valid_email(text):
		with db.connection.cursor() as cursor:
			sql = "INSERT INTO `halls` (`name`) VALUES (%s)"
			cursor.execute(sql, (text.strip().lower()))
	
	print(phone_to_int(sender))
	print(text)
	return text

def phone_to_int(str_phone_number): # convert '+12345678910' into 12345678910
	return int(str_phone_number[1:])

def phone_to_str(int_phone_number): # convert 12345678910 into '+12345678910'
	return '+'+str(int_phone_number)

def is_valid_email(email): # method to check if given email is valid format
	pattern = "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$"
	if re.match(pattern, email.strip()) != None:
		return True
	return False