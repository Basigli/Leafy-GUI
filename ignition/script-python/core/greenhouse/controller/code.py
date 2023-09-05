def get_greenhouses():
	return frwk.framework.tags.get_formatted_tags('[default]GreenHouses')


def log_greenhouses_input_sensors():
	"""
	Saves input sensors data into the db

	Args:
		* none
	Returns:
		none
	"""
	greenhouses = get_greenhouses()
	
	for i, greenhouse in greenhouses.items():
		greenhouse_id = greenhouse.get('Id').get_value()
		air_hum = greenhouse.get('AirHumidity').get_value()
		air_temp = greenhouse.get('AirTemperature').get_value()
		light_quantity = greenhouse.get('LightQuantity').get_value()
		terrain_hum = greenhouse.get('TerrainHumidity').get_value()
		is_tank_empty = greenhouse.get('IsTankEmpty').get_value()
		
		frwk.db.database.log_input_sensors(greenhouse_id, air_hum, air_temp, light_quantity, terrain_hum, is_tank_empty)
		
		
def log_greenhouses_output_actuators():
	"""
	Saves input sensors data into the db

	Args:
		* none
	Returns:
		none
	"""	
	greenhouses = get_greenhouses()
	
	for i, greenhouse in greenhouses.items():
		greenhouse_id = greenhouse.get('Id').get_value()
		irrigation_pump = greenhouse.get('IrrigationPump').get_value()
		uv_light = greenhouse.get('UVLight').get_value()
		ventilation = greenhouse.get('Ventilation').get_value()
		frwk.db.database.log_output_actuators(greenhouse_id, irrigation_pump, uv_light, ventilation)
	
			
def get_formatted_sensor_data(greenhouse_id, sensor_name, start_date, end_date):
	"""
	Retrieves from db data of a given sensor

	Args:
		* greenhouse_id (int):
		* sensor_name (str) 
		* start_date (date):
		* end_date (date):
		
	Returns:
		none
	"""
	data = []
	raw_data = frwk.db.database.get_sensors_data(greenhouse_id, start_date, end_date)
	
	for row in raw_data:
		item = {
			sensor_name: row[sensor_name],
			't_stamp': row['timeStamp']
		}
		data.append(item)
	return data


def get_formatted_actuator_data(greenhouse_id, actuator_name, start_date, end_date):
	"""
	Retrieves from db data of a given actuator

	Args:
		* greenhouse_id (int):
		* actuator_name (str) 
		* start_date (date):
		* end_date (date):
		
	Returns:
		none
	"""
	data = []
	raw_data = frwk.db.database.get_actuators_data(greenhouse_id, start_date, end_date)
	for row in raw_data:
		item = {
			actuator_name: row[actuator_name],
			't_stamp': row['timeStamp']
		}
		data.append(item)
	return data


def get_greenhouse_from_id(greenhouse_id):
	greenhouses = get_greenhouses()
	try:
		return greenhouses[greenhouse_id]
	except:
		import traceback
		core.utils.logger.exc('get_greenhouse_from_id', traceback.format_exc())
		return {}


def write_tag(tag_path, value):
	system.tag.writeBlocking(tag_path, [value])


def turn_off(greenhouse_id, actuator_name):
	
	greenhouse = get_greenhouse_from_id(str(greenhouse_id))
	
	actuator_tag_path = greenhouse[actuator_name].tag_path
	try:
		write_tag(actuator_tag_path, False)
		log_greenhouses_output_actuators()
		core.utils.logger.info('turn_off()', 'turned off {} for greenhouse: {}'.format(actuator_name, greenhouse_id))
		return True
	except:
		import traceback
		core.utils.logger.exc('turn_off()', traceback.format_exc())
		return False


def turn_on(greenhouse_id, actuator_name):
	
	greenhouse = get_greenhouse_from_id(str(greenhouse_id))
	
	actuator_tag_path = greenhouse[actuator_name].tag_path
	try:
		write_tag(actuator_tag_path, True)
		log_greenhouses_output_actuators()
		core.utils.logger.info('turn_on()', 'turned on {} for greenhouse: {}'.format(actuator_name, greenhouse_id))
		return True
	except:
		import traceback
		core.utils.logger.exc('turn_on()', traceback.format_exc())
		return False


def get_all_formatted_greenhouse():
	greenhouses = get_greenhouses()
	return [{'label': value['Name'].get_value(), 'value': value['Id'].get_value()} for key, value in greenhouses.items()]


def create_or_override_tag(tag_path, name, value):
	tag_type=frwk.configurations.base.get_type(value)
	if tag_type == 'Document':
		value = system.util.jsonEncode(value)
	if tag_type == 'DateTime':
		value =  system.date.format(value)
	tag = {
		"name": name,           
		"tagType": "AtomicTag",
		"valueSource": "memory",
		"value": value,
		"dataType": tag_type
	}
	
	collisionPolicy = "o"
				 
	# Create the tag.
	system.tag.configure(tag_path, [tag], collisionPolicy)


def greenhouse_auto_mode(greenhouse):
	pass


def greenhouses_auto_mode():
	greenhouses = get_greenhouses()


def get_new_preset_id():
	preset_id_path = '[default]Config/CurrentPresetId'
	current_preset_id = system.tag.readBlocking(preset_id_path)[0].value
	
	system.tag.writeBlocking(preset_id_path, current_preset_id + 1)
	return str(current_preset_id + 1)


def save_preset_to_tag(preset):
	preset_id = get_new_preset_id()
	base_path = '[default]Presets/' + preset_id
	create_or_override_tag(base_path, 'Description', str(preset['Description']))
	create_or_override_tag(base_path, 'Name', str(preset['Name']))
	create_or_override_tag(base_path, 'StagesNumber', preset['StagesNumber'])
	
	stages_path = base_path + '/Stages'
	
	for stage_number in range(1, preset['StagesNumber'] + 1):
		stage_path = stages_path + '/' + str(stage_number)
		stage = preset['Stages'][str(stage_number)]
		create_or_override_tag(stage_path, 'StartDate', stage['StartDate'])
		create_or_override_tag(stage_path, 'EndDate', stage['EndDate'])
		
		#Ventilation
		ventilation_path = stage_path + '/Ventilation'
		ventilation = stage['Ventilation']
		create_or_override_tag(ventilation_path, 'EndTime', ventilation['EndTime'])
		try:
			create_or_override_tag(ventilation_path, 'HighSetpoint', int(ventilation['HighSetpoint']))
		except:
			create_or_override_tag(ventilation_path, 'HighSetpoint', 0)
		create_or_override_tag(ventilation_path, 'IsTemp', ventilation['IsTemp'])
		try:
			create_or_override_tag(ventilation_path, 'LowSetpoint', int(ventilation['LowSetpoint']))
		except:
			create_or_override_tag(ventilation_path, 'LowSetpoint', 0)
		create_or_override_tag(ventilation_path, 'StartTime', ventilation['StartTime'])
		
		#UVLight
		UVLight_path = stage_path + '/UVLight'
		UVLight = stage['UVLight']
		create_or_override_tag(UVLight_path, 'EndTime', UVLight['EndTime'])
		try:
			create_or_override_tag(UVLight_path, 'HighSetpoint', int(UVLight['HighSetpoint']))
		except:
			create_or_override_tag(UVLight_path, 'HighSetpoint', 0)
		create_or_override_tag(UVLight_path, 'IsTemp', UVLight['IsTemp'])
		try:
			create_or_override_tag(UVLight_path, 'LowSetpoint', int(UVLight['LowSetpoint']))
		except:
			create_or_override_tag(UVLight_path, 'LowSetpoint', 0)
		create_or_override_tag(UVLight_path, 'StartTime', UVLight['StartTime'])

		#IrrigationPump
		irrigation_path = stage_path + '/IrrigationPump'
		irrigation = stage['IrrigationPump']
		create_or_override_tag(irrigation_path, 'EndTime', irrigation['EndTime'])
		try:
			create_or_override_tag(irrigation_path, 'HighSetpoint', int(irrigation['HighSetpoint']))
		except:
			create_or_override_tag(irrigation_path, 'HighSetpoint', 0)
		create_or_override_tag(irrigation_path, 'IsTemp', irrigation['IsTemp'])
		try:
			create_or_override_tag(irrigation_path, 'LowSetpoint', int(irrigation['LowSetpoint']))
		except:
			create_or_override_tag(irrigation_path, 'LowSetpoint', 0)
		create_or_override_tag(irrigation_path, 'StartTime', irrigation['StartTime'])


def get_formatted_presets_list():
	"""
	For GUI use only.
	"""
	presets = frwk.framework.tags.get_formatted_tags('[default]Presets')
	
	presets_list = []
	
	for preset_id, preset in presets.items():
		presets_list.append({
			'presetId': preset_id,
			'name': preset['Name'].get_value(),
			'description': preset['Description'].get_value()
		})
	
	return presets_list


def delete_preset(preset_id):
	presets_path = '[default]Presets'
	
	
	system.tag.deleteTags([presets_path + '/' + preset_id])




