import json, pymysql

# Get Configuration file keys.json and store values in the variable 'keys'
try:keys = json.loads(open('helpers/keys.json').read())
except:raise FileNotFoundError("Configuration file keys.json not found, contact the owner to get access!")

connection = pymysql.connect(keys['db_host'],keys['db_user'],keys['db_pass'],keys['db_name'])


# ALL CUSTOM METHODS TO PULL DATA FROM DATABASE GOES HERE

def format_sql_result(lst):
	result = []
	for next in lst:
		result.append(next[0])
	return result

#Is given a string containing floor_ids and returns a list of 
#phone numbers of students living on those floors.
def get_phone_nums(floor_ids):
	floor_ids = floor_ids.split(',')

	with connection.cursor() as cursor:
		format_strings = ','.join(['%s'] * len(floor_ids))
		cursor.execute("SELECT phone FROM students where floor_id IN (%s)" % format_strings, tuple(floor_ids))
		result = cursor.fetchall()

	result = format_sql_result(result)
	print(result)
	return result
	

get_phone_nums("2")