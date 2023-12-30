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
			return system.db.runPrepUpdate(query, values.values(), database=self.connection_name, getKey=1)
		except:
			import traceback
	    	try:
	    		print(traceback.format_exc())
	    	except:
	    		pass
		return None
		
	def _get(self, where):
		pass
		
	def _get_from_id(self, id):
		pass
		
	def _update(self, where):
		pass
	
	def _update_from_id(self, id):
		pass