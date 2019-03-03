from datetime import datetime

#floor_ids_list is a list where an element can be floor id
#or a list of floor ids as strings. 
#This method returns a string containing floor ids(dot separated values) where each floor id is unique
#and moreover, the list(string) is sorted.
def format_floor_ids(floor_ids_list):
	#first flatten out an array.
	flat_list = '.'.join(floor_ids_list)
	flat_list = flat_list.split('.')
	
	#then sort the unique elements.
	result = sorted(set(flat_list), key=lambda x: int(x))

	return ".".join(result)

def format_data_times(list_of_data, time_index=8):# time_index Needed Wildcard 
	for data in list_of_data:
		my_time = data[time_index]
		date_diff = (datetime.now().date()-my_time.date()).days
		if date_diff == 0:
			format = "%-I:%M %p" # 2:15 pm
		elif date_diff < 7:
			format = "%a %-I:%M %p" # SAT 4:32 pm
		else:
			format = "%b %-d %-I:%M %p" # Mar 2 8:44 pm
		data[time_index] = datetime.strftime(my_time, format)
	return list_of_data