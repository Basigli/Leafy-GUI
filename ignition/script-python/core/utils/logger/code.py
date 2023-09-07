import traceback 


def exc(function_name, description=''):
	"""
	Records an exception log entry in the database and returns True if the action is successful, otherwise returns False.
	
	Args:
	    * function_name (str): The name of the function that generated the exception.
	    * description (str): An optional description of the exception.
	
	Returns:
	    bool: True if the action is successfully executed, and the log is recorded in the database, False otherwise.
	
	Notes:
	    This function logs an entry of type 'Exception' in the database using the provided arguments. If the logging operation succeeds, the function returns True. In case of an error during database logging, an error message will be printed, and the function returns False.
	"""
	args = {
		'functionName': function_name,
		'timestamp': system.date.now(),
		'description': description,
		'type': 'Exception'
	}
	try:
		system.db.runNamedQuery('InsertIntoLOGGER', args)
		return True
	except:
		print('error in query: ' + traceback.format_exc())
		return False


def err(function_name, description=''):
	"""
	Records an error log entry in the database and returns True if the action is successful, otherwise returns False.
	
	Args:
	    * function_name (str): The name of the function associated with the error.
	    * description (str): An optional description of the error.
	
	Returns:
	    bool: True if the action is successfully executed, and the error log is recorded in the database, False otherwise.
	
	Notes:
	    This function logs an entry of type 'Error' in the database using the provided arguments. If the logging operation succeeds, the function returns True. In case of an error during database logging, an error message will be printed, and the function returns False.
	"""
	args = {
		'functionName': function_name,
		'timestamp': system.date.now(),
		'description': description,
		'type': 'Error'
	}
	try:
		system.db.runNamedQuery('InsertIntoLOGGER', args)
		return True
	except:
		print('error in query: ' + traceback.format_exc())
		return False


def info(function_name, description=''):
	"""
	Records an information log entry in the database and returns True if the action is successful, otherwise returns False.
	
	Args:
	    * function_name (str): The name of the function associated with the information log entry.
	    * description (str): An optional description of the information.
	
	Returns:
	    bool: True if the action is successfully executed, and the information log is recorded in the database, False otherwise.
	
	Notes:
	    This function logs an entry of type 'Info' in the database using the provided arguments. If the logging operation succeeds, the function returns True. In case of an error during database logging, an error message will be printed, and the function returns False.
	"""
	args = {
		'functionName': function_name,
		'timestamp': system.date.now(),
		'description': description,
		'type': 'Info'
	}
	try:
		system.db.runNamedQuery('InsertIntoLOGGER', args)
		return True
	except:
		print('error in query: ' + traceback.format_exc())
		return False