import traceback 


def exc(function_name, description=''):
	"""
	Insert an exception type log into the db

	Args:
		* function_name (str): name of the function
		* description (str): optional description 
	Returns:
		True if the action is performed, False otherwise 
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
	Insert an error type log into the db

	Args:
		* function_name (str): name of the function
		* description (str): optional description 
	Returns:
		True if the action is performed, False otherwise 
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
	Insert an info type log into the db

	Args:
		* function_name (str): name of the function
		* description (str): optional description 
	Returns:
		True if the action is performed, False otherwise 
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