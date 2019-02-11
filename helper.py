import json, sqlite3 as sql
from twilio.rest import Client

keys = json.loads(open('keys.json').read())

def create_client():
	account_sid = keys['account_sid']
	auth_token = keys['auth_token']
	return Client(account_sid, auth_token)

def send_message(receiver, text):
	client = create_client()
	sender = keys['phone_number']
	message = client.messages.create(from_=sender, body=text, to=receiver)
	return message

def process_response(sender, text):
	print(phone_to_int(sender))
	return text

def phone_to_int(str_phone_number): # convert '+12345678910' into 12345678910
	return int(str_phone_number[1:])

def phone_to_str(int_phone_number): # convert 12345678910 into '+12345678910'
	return '+'+str(int_phone_number)

def connect_db(db=keys['database']): # connect to my sqlite database
	con = sql.connect(db)
	return con

def migration():
	with connect_db() as con:
		query = 'CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)'
		con.execute(query)
	print("Migration is successul on query:",query)


