def get_greenhouses():
	"""
	Retrieves a dictionary of greenhouse tags with greenhouse IDs as keys.
	
	Returns:
	    dict: A dictionary where keys are greenhouse IDs and values are formatted greenhouse tags.
	
	Notes:
	    This function retrieves a dictionary of greenhouse tags, where each tag is associated with a specific greenhouse ID. The dictionary is typically used to map greenhouse IDs to their corresponding tags, providing a convenient way to access information about available greenhouses within the system.
	"""
	return frwk.framework.tags.get_formatted_tags('[default]GreenHouses')


def log_greenhouses_input_sensors():
	"""
	Saves input sensor data for all greenhouses into the database.
	
	Args:
	    None
	
	Returns:
	    None
	
	Notes:
	    This function retrieves input sensor data for all greenhouses, including air humidity, air temperature, light quantity, terrain humidity, and tank status. It then logs this data into the database for each greenhouse. There are no arguments, and the function doesn't return anything.
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
	Saves output actuator data for all greenhouses into the database.
	
	Args:
	    None
	
	Returns:
	    None
	
	Notes:
	    This function retrieves output actuator data for all greenhouses, including irrigation pump status, UV light status, and ventilation status. It then logs this data into the database for each greenhouse. There are no arguments, and the function doesn't return anything.
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
	Retrieves sensor data for a specific sensor in a greenhouse from the database.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse for which sensor data is requested.
	    * sensor_name (str): The name of the sensor for which data is requested.
	    * start_date (date): The start date of the data retrieval period.
	    * end_date (date): The end date of the data retrieval period.
	
	Returns:
	    list: A list of dictionaries containing sensor data for the specified sensor within the specified date range.
	
	Notes:
	    This function retrieves sensor data for a specific sensor in a greenhouse from the database. It takes the greenhouse ID, sensor name, and date range as arguments and returns the data in a formatted list of dictionaries. Each dictionary includes the sensor data and its timestamp.
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
    Retrieves actuator data for a specific actuator in a greenhouse from the database.

    Args:
        * greenhouse_id (int): The ID of the greenhouse for which actuator data is requested.
        * actuator_name (str): The name of the actuator for which data is requested.
        * start_date (date): The start date of the data retrieval period.
        * end_date (date): The end date of the data retrieval period.

    Returns:
        list: A list of dictionaries containing actuator data for the specified actuator within the specified date range.

    Notes:
        This function retrieves actuator data for a specific actuator in a greenhouse from the database. It takes the greenhouse ID, actuator name, and date range as arguments and returns the data in a formatted list of dictionaries. Each dictionary includes the actuator data and its timestamp.
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
	"""
	Retrieves information about a specific greenhouse based on its ID.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse for which information is requested.
	
	Returns:
	    dict: A dictionary containing information about the specified greenhouse, or an empty dictionary if the greenhouse is not found.
	
	Notes:
	    This function retrieves information about a specific greenhouse based on its ID. It takes the greenhouse ID as an argument and returns a dictionary containing greenhouse information, including tags and attributes. If the specified greenhouse ID is not found, an empty dictionary is returned.
	"""
	greenhouses = get_greenhouses()
	try:
		return greenhouses[greenhouse_id]
	except:
		import traceback
		core.utils.logger.exc('get_greenhouse_from_id', traceback.format_exc())
		return {}


def write_tag(tag_path, value):
	"""
	Writes a value to a specified tag in the system.
	
	Args:
	    * tag_path (str): The path to the tag that needs to be written.
	    * value: The value to be written to the tag.
	
	Returns:
	    None
	
	Notes:
	    This function is used to write a value to a specific tag in the system. It takes the tag's path as a string and the value to be written. The function performs a blocking write operation to update the tag's value. It does not return any value.
	"""
	system.tag.writeBlocking(tag_path, [value])


def turn_off(greenhouse_id, actuator_name):
	"""
	Turns off an actuator for a specific greenhouse.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse for which the actuator needs to be turned off.
	    * actuator_name (str): The name of the actuator to be turned off.
	
	Returns:
	    bool: True if the actuator is successfully turned off, False otherwise.
	
	Notes:
	    This function turns off a specified actuator for a specific greenhouse. It retrieves the actuator's tag path based on the greenhouse ID and actuator name, writes a 'False' value to the tag to turn off the actuator, and logs the action. If successful, it returns True; otherwise, it returns False.
	    """
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
	"""
	Turns on an actuator for a specific greenhouse.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse for which the actuator needs to be turned on.
	    * actuator_name (str): The name of the actuator to be turned on.
	
	Returns:
	    bool: True if the actuator is successfully turned on, False otherwise.
	
	Notes:
	    This function turns on a specified actuator for a specific greenhouse. It retrieves the actuator's tag path based on the greenhouse ID and actuator name, writes a 'True' value to the tag to turn on the actuator, and logs the action. If successful, it returns True; otherwise, it returns False.
	"""
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
	"""
	Retrieves information about all greenhouses in a formatted list.

    Returns:
        list: A list of dictionaries containing information about all greenhouses, including labels (names) and values (IDs).

    Notes:
        This function retrieves information about all greenhouses and formats it into a list of dictionaries. Each dictionary contains a 'label' representing the greenhouse name and a 'value' representing the greenhouse ID. It provides a convenient way to access and display information about all greenhouses within the system.
    """
	greenhouses = get_greenhouses()
	return [{'label': value['Name'].get_value(), 'value': value['Id'].get_value()} for key, value in greenhouses.items()]


def create_or_override_tag(tag_path, name, value):
	"""
	Creates or overrides a tag at the specified path with the given name and value.
	
	Args:
	    * tag_path (str): The path where the tag should be created or overridden.
	    * name (str): The name of the tag.
	    * value: The value to be assigned to the tag.
	
	Returns:
	    None
	
	Notes:
	    This function creates a new tag or overrides an existing tag at the specified path. It takes the tag's path, name, and value as arguments and determines the tag's data type based on the provided value. It then configures the tag with the specified attributes, including the data type, name, and value. If a tag already exists at the specified path, it will be overridden with the new configuration.
	"""
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
	# Create the tag or override the existing tag.	
	system.tag.configure(tag_path, [tag], collisionPolicy)


def get_presets():
	"""
	Retrieves a list of formatted configuration presets.
	
	Returns:
	    dict: A dictionary containing configuration presets with their unique IDs as keys.
	
	Notes:
	    This function retrieves a dictionary of formatted configuration presets. It collects preset data from tags in the system and formats it as a dictionary, where each key represents a unique preset ID. This collection of presets can be used to manage and access configuration presets in the system.
	""" 
	return frwk.framework.tags.get_formatted_tags('[default]Presets')
 	
 	
def get_preset_from_id(preset_id):
 	"""
    Retrieves a configuration preset based on its ID.

    Args:
        * preset_id (str): The ID of the configuration preset to be retrieved.

    Returns:
        dict: A dictionary containing information about the specified configuration preset, or an empty dictionary if the preset is not found.

    Notes:
        This function retrieves a configuration preset from the system based on its unique ID. It takes the preset ID as an argument and returns a dictionary containing information about the specified preset. If the preset ID is not found, an empty dictionary is returned.
    """
 	presets = get_presets()
 	return presets[str(preset_id)]


def get_current_stage(stages):
	"""
    Retrieves the current stage from a dictionary of stages based on the current date and time.

    Args:
		* stages (dict): A dictionary containing stage information with stage numbers as keys.

    Returns:
        int or dict: The current stage number or a dictionary containing information about the current stage. Returns -1 if no current stage is found.

    Notes:
        This function determines the current stage from a dictionary of stages by comparing the current date and time with the start and end dates of each stage. It returns the current stage number or a dictionary with stage details if a current stage is found. If no current stage is found or an error occurs, it returns -1.
    """

	now = system.date.now()
	now_millis = system.date.toMillis(now)
	
	if len(stages.keys()) < 1:
		return -1
	
	for stage_number, stage in stages.items():
		try:
			if(now_millis  >= system.date.toMillis(stage['StartDate'].get_value()) and now_millis < system.date.toMillis(stage['EndDate'].get_value())):
				return stage
		except:
			import traceback
			core.utils.logger.exc('get_current_stage', traceback.format_exc())
	
	return -1

##----------------- TO DO -------------------------------
def greenhouse_auto_mode(greenhouse):
	current_preset_id = greenhouse['PresetId']
	current_preset = get_preset_form_id(current_preset_id)
	stages_number = current_preset['StagesNumber']
	stages = current_preset['Stages']
	current_stage = get_current_stage(stages)
	
	


def greenhouses_auto_mode():
	"""
    Activates automatic mode for greenhouses.

    Returns:
        None

    Notes:
        This function enables automatic mode for greenhouses by iterating through all available greenhouses in the system. It checks the 'Auto' status for each greenhouse, and if it is set to True, it activates the automatic mode for that specific greenhouse by calling the 'greenhouse_auto_mode' function. Automatic mode typically involves managing and controlling various environmental parameters and actuators within the greenhouse.
    """
	greenhouses = get_greenhouses()
	for i, greenhouse in greenhouses.items():
		auto_mode = greenhouse.get('Auto').get_value()
		if auto_mode:
			greenhouse_auto_mode(greenhouse)
	
	
##-------------------------------------------------------

def get_new_preset_id():
	"""
    Retrieves and increments the current preset ID for configuration.

    Returns:
    	* str: A string representing the new preset ID.

    Notes:
        This function retrieves the current preset ID for configuration from a specified path. It increments the current ID by 1 and writes the updated ID back to the same path. The new preset ID is returned as a string. This function is typically used to generate unique IDs for configuration presets.
    """
	preset_id_path = '[default]Config/CurrentPresetId'
	current_preset_id = system.tag.readBlocking(preset_id_path)[0].value
	
	system.tag.writeBlocking(preset_id_path, current_preset_id + 1)
	return str(current_preset_id + 1)


def save_preset_to_tag(preset):
	"""
	Saves a configuration preset to tags in the system.
	
	Args:
	    * preset (dict): A dictionary containing configuration preset data.
	
	Returns:
	    None
	
	Notes:
	    This function takes a dictionary representing a configuration preset and saves it to tags in the system. It creates or overrides tags with preset data, including description, name, number of stages, stage details, and specific settings for ventilation, UV light, and irrigation pump for each stage. The function is typically used to store and manage configuration presets in the system.
	"""
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
	Retrieves a list of formatted configuration presets for GUI use.
	
	Returns:
	    list: A list of dictionaries containing information about configuration presets, including preset ID, name, and description.
	
	Notes:
	    This function is intended for GUI use and retrieves a list of formatted configuration presets. It collects preset data from tags in the system and formats it into a list of dictionaries. Each dictionary contains information about a configuration preset, including its preset ID, name, and description. This list can be used to display and select presets within a graphical user interface.
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
	"""
	Deletes a configuration preset based on its ID.
	
	Args:
	    * preset_id (str): The ID of the configuration preset to be deleted.
	
	Returns:
	    None
	
	Notes:
	    This function deletes a configuration preset from the system based on its unique ID. It takes the preset ID as an argument and removes the corresponding tag associated with that preset from the system. After calling this function, the specified configuration preset will no longer be available in the system.
	"""
	presets_path = '[default]Presets'
	system.tag.deleteTags([presets_path + '/' + preset_id])




