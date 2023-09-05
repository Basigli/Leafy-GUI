CONFIG_TABLE = 'frwk_companies_config'
CONNECTION = 'IgnitionCFG'

def cast(val, new_type):
	"""
	Casts the value to the new type (if possibile).
	New type can either be:
		* int
		* str
		* float
		* bool
		
	Args:
		* val (any): the value to cast
		* new_type (str): the type to cast value to
		
	Returns:
		Type matching new_type string
	"""
	switcher = {
		'int': int,
		'str': str,
		'float': float,
		'bool': lambda x: bool(x) and x != '0'
	}
	return switcher[new_type](val)
	
	
def get_type(val):
	"""
	Retrieves the type of the value as a string
	
	Args:
		val (any): the value we are interested to know the
				   type of
				   
	Returns:
		Str. String indicating the type
	"""
	switcher = {
		int: 'Int4',
		long: 'Int8',
		str: 'String',
		float: 'Float',
		bool: 'Boolean'
	}
	if 'java.util.Date' in str(type(val)):
		return 'DateTime'
	return switcher.get(type(val), 'Document')


class BaseConfig(object):
	def __init__(self, defaults, internal_values):
		self.defaults = defaults
		self.internal_values = internal_values
		self.init()
	
	def init(self):
		for key in self.defaults.keys():
			if not self.has_key(key):
				value = self.defaults[key]
				self[key] = value
		
	def keys(self):
		return self.defaults.keys() + self.internal_values.keys()
	
	def get_all(self):
		return {key: self[key] for key in self.keys()}

	def _get_or_default_(self, key):
		pass
		
	def _set_or_make_(self, key, value):
		pass

	def __getitem__(self, key):
		if key in self.internal_values.keys():
			return self.internal_values[key]
		else:
			return self._get_or_default_(key)
			
	def __setitem__(self, key, value):
		self._set_or_make_(key, value)
		
	def has_key(self, key):
		pass


class DBConfig(BaseConfig):
	def __init__(self, defaults, table=CONFIG_TABLE, connection=CONNECTION):
		internal_values = {
			'config': table,
			'connection': connection
		}
		BaseConfig.__init__(self, defaults, internal_values)
		
	def _get_or_default_(self, key):
		query = "SELECT TOP(1) \"Value\", \"Type\" FROM %s WHERE \"Key\" = ?" % self['config']
		args = (key,)
		
		res = system.db.runPrepQuery(query, args, database=self.connection)
		if res.getRowCount() > 0:
			value = res.getValueAt(0, 'Value')
			type = res.getValueAt(0, 'Type')
			return cast(value, type)
		else:
			return self.defaults[key]
		
	def _set_or_make_(self, key, value):
		# Check if record exists
		query = "SELECT TOP(1) \"Value\", \"Type\" FROM %s WHERE \"Key\" = ?" % self['config']
		args = (key,)
		res = system.db.runPrepQuery(query, args, database=self.connection)
		exitsts = res.getRowCount() > 0
		
		if exists:
			query = "UPDATE %s SET \"Value\" = ? WHERE \"Key\" = ?" % self['config']
		else:
			query = "INSERT INTO %s (\"Value\", \"Key\") VALUES (?, ?)" % self['config']
		args = (value, key)
		
		system.db.runPrepQuery(query, args, database=self.connection)
		
	def has_key(self, key):
		query = "SELECT COUNT(*) FROM %s WHERE \"Key\" = ?" % self['config']
		args = (key,)
		res = system.db.runScalarPrepQuery(query, args, database=self.connection)
		return res > 1


class TagConfig(BaseConfig):
	def __init__(self, defaults, path):
		internal_values = {
			'path': path,
		}
		BaseConfig.__init__(self, defaults, internal_values)
		
	def __create_or_override(self, name, value):
		tag_type = get_type(value)
		if tag_type == 'Document':
			value = system.util.jsonEncode(value)
		tag = {
			"name": name,           
			"tagType": "AtomicTag",
			"valueSource": "memory",
			"value": value,
			"dataType": tag_type
		}
		
		collisionPolicy = "o"
					 
		# Create the tag.
		system.tag.configure(self['path'], [tag], collisionPolicy)
		
	def _get_or_default_(self, key):
		full_path = self['path'] + '/' + key
		if system.tag.exists(full_path):
			value = system.tag.read(full_path).value
		else:
			value = self.defaults[key]
			self.__create_or_override(key, value)
		
		if str(system.tag.getConfiguration(full_path)[0]['dataType']) == 'Document':
			value = system.util.jsonDecode(value)
		return value
		
	def _set_or_make_(self, key, value):
		self.__create_or_override(key, value)
		
	def has_key(self, key):
		return system.tag.exists(self['path'] + '/' + key)