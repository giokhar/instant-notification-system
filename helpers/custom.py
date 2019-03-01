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