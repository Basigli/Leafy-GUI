class Logger(frwk.db.classes.DBObject):
	def __init__(self, function_name='Logger'):
		self.function_name = function_name
		self.table_name = frwk.db.constants.Tables.LOGGER
		self.connection_name = frwk.db.constants.DEFAUL_DATABASE
	
	def exc(self, description):
		values = {
			'functionName': self.function_name,
			'timestamp': system.date.now(),
			'description': description,
			'type': 'Exception'
		}	
		self._insert(values)
	
	def err(self, description):
		values = {
			'functionName': self.function_name,
			'timestamp': system.date.now(),
			'description': description,
			'type': 'Error'
		}	
		self._insert(values)
	
	def info(self, description):
		values = {
			'functionName': self.function_name,
			'timestamp': system.date.now(),
			'description': description,
			'type': 'Info'
		}	
		self._insert(values)