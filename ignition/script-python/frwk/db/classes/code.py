class DBObject:
	def __init__(self, table_name, connection_name=frwk.db.constants.DEFAUL_DATABASE):
	    self.table_name = table_name
	    self.connection_name = connection_name
	
	def _insert(self, values):
		"""
		Inserts into the database a tuple
		
		Args:
			* values (dict):a dictonary with the name of the columns as keys and the associated values
		
		Returns:
			bool: true or false depending on the success of the operation
			
		Notes:
			None
		"""
		query = "INSERT INTO %s(%s) VALUES \n%s" % (
			    	self.table_name, 
			    	", ".join(map(lambda value: "%s" % value, values.keys())), 
			    	"(%s)" % ", ".join(map(lambda x: "?", values.keys()))ù
			    	)
		try:
			system.db.runPrepUpdate(query, values.values(), database=self.connection_name, getKey=True)
			return True
		except:
			import traceback
	    	try:
	    		print(traceback.format_exc())
	    	except:
	    		pass
		return False

	def _get(self, where, values):
		"""
		Runs a query on the database
				
		Args:
			* where (str):the SQL WHERE clause, with ? instead of the actual values, it should be well formatted
			* values (arr):the array containing the values in the WHERE clasue, the values should be in the same order of the where variable
			
		Returns:
			pyDataSet: a pyDataSet conteining the result of the query or empty in case of error
					
		Notes:
			The where variable should be a string formatted as and SQL statement, and the values inside the variable values should be in the
			same order as the parameters passed in the where variable
		"""
		query = "SELECT * FROM %s WHERE %s" % (self.table_name, where)
		try:
			return system.db.runPrepQuery(query, values, database=self.connection_name)
		except:
			import traceback
			try:
				print(traceback.format_exc())
			except:
				pass
		return system.dataset.toPyDataSet(system.dataset.toDataSet([], []))
	
	def _get_from_id(self, id):
		"""
		Runs a query on the database on a specific tuple id
				
		Args:
			* id (int): the id(primary key) of the tuple you want to retrieve from the database
			
		Returns:
			pyDataSet: a pyDataSet conteining the result of the query or empty in case of error
					
		Notes:
			The id is a primary key so this funcion can at most retrieve one specific tuple
		"""
		query = "SELECT * FROM %s WHERE id = ?" % (self.table_name)
		try:
			return system.db.runPrepQuery(query, [id], database=self.connection_name)
		except:
			import traceback
			try:
				print(traceback.format_exc())
			except:
				pass
		return system.dataset.toPyDataSet(system.dataset.toDataSet([], []))

	def _update(self, values, where_id):
		"""
		!!DA FINIRE!! Runs an SQL update statement against the database
				
		Args:
			* values (dict): the keys in the dictonary should be the name of columns to update, the associated values should be the new values to update
			* where_id (int): the id(primary key) of a specific tuple in the databse
		Returns:
			bool: true or false depending on the succsess of the operation
					
		Notes:
			The id is a primary key so this funcion can at most update one specific tuple
		"""
		update = "UPDATE %s SET %s WHERE id = ?" % (self.table_name, ", ".join(map(lambda value: "%s" % value, values.keys())),
		)
		
		try:
			system.db.runPrepUpdate(update, where_id, database=self.connection_name)
			return True
		except:
			import traceback
			try:
				print(traceback.format_exc())
			except:
				pass
		return False
		