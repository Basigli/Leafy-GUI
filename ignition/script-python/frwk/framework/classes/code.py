class FormattedTag:
	def __init__(self, tag_path, is_folder, display_name=None, unit=None, is_historical=None):
		self.tag_path = tag_path
		self.name = tag_path.split('/')[-1]
		self.is_folder = is_folder
		self.display_name = display_name
		self.unit = unit
		self.is_historical = is_historical
		#self.cfg = system.tag.getConfiguration(self.tag_path)[0]
	
	def get_value(self):
		return system.tag.readBlocking(self.tag_path)[0].value
	
	
	def get_name(self):
		if self.display_name is not None:
			return self.display_name
		cfg = system.tag.getConfiguration(self.tag_path)[0]
		return cfg.get('description', cfg['name'])
		
	def get_unit(self):
		if self.unit is not None:
			return self.unit
		cfg = system.tag.getConfiguration(self.tag_path)[0]
		return cfg.get('engUnit', '')
	
	def history_enabled(self):
		if self.is_historical is not None:
			return self.is_historical
		cfg = system.tag.getConfiguration(self.tag_path)[0]
		return cfg.get('historyEnabled', False)
		
	def get_configuration(self):
		return system.tag.getConfiguration(self.tag_path)
		
	def to_payload(self):
		return {
			'fullPath': self.tag_path,
			'actualName': self.name,
			'name': self.get_name(),
			'unit': self.get_unit(),
			'isFolder': self.is_folder
		}
