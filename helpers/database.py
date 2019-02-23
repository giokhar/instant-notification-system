import json, pymysql

# Get Configuration file keys.json and store values in the variable 'keys'
try:keys = json.loads(open('helpers/keys.json').read())
except:raise FileNotFoundError("Configuration file keys.json not found, contact the owner to get access!")

connection = pymysql.connect(keys['db_host'],keys['db_user'],keys['db_pass'],keys['db_name'])


# ALL CUSTOM METHODS TO PULL DATA FROM DATABASE GOES HERE

#Is given a list of floor_ids and returns a list of 
#phone numbers of those students who live in floors with
def get_phone_nums(floor_ids):

with connection.cursor() as cursor:
	cursor.execute('SELECT * FROM students')

	result = cursor.fetchall()

print(result)