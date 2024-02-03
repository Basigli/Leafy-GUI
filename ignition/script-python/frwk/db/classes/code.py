class DBObject:
	def __init__(self, table_name, connection_name=frwk.db.constants.DEFAUL_DATABASE):
	    self.table_name = table_name
	    self.connection_name = connection_name
	
	def _insert(self, values):
		query = "INSERT INTO %s(%s) VALUES \n%s" % (
			    	self.table_name, 
			    	", ".join(map(lambda value: "%s" % value, values.keys())), 
			    	"(%s)" % ", ".join(map(lambda x: "?", values.keys()))
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
		update = "UPDATE %s SET %s WHERE id = ?" % (self.table_name, values)
		
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
		