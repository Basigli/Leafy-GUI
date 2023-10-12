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
	    This function retrieves output actuator data for all greenhouses, including irrigation pump status, UV light status, and ventilation status. 
	    It then logs this data into the database for each greenhouse. There are no arguments, and the function doesn't return anything.
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
	    This function retrieves sensor data for a specific sensor in a greenhouse from the database. 
	    It takes the greenhouse ID, sensor name, and date range as arguments and returns the data in a formatted list of dictionaries. 
	    Each dictionary includes the sensor data and its timestamp.
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
        This function retrieves actuator data for a specific actuator in a greenhouse from the database. 
        It takes the greenhouse ID, actuator name, and date range as arguments and returns the data in a formatted list of dictionaries. 
        Each dictionary includes the actuator data and its timestamp.
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
	    * greenhouse_id (str): The ID of the greenhouse for which information is requested.
	
	Returns:
	    dict: A dictionary containing information about the specified greenhouse, or an empty dictionary if the greenhouse is not found.
	
	Notes:
	    This function retrieves information about a specific greenhouse based on its ID. 
	    It takes the greenhouse ID as an argument and returns a dictionary containing greenhouse information, including tags and attributes. 
	    If the specified greenhouse ID is not found, an empty dictionary is returned.
	"""
	greenhouses = get_greenhouses()
	try:
		return greenhouses[str(greenhouse_id)]
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
	    This function is used to write a value to a specific tag in the system. It takes the tag's path as a string and the value to be written. 
	    The function performs a blocking write operation to update the tag's value. It does not return any value.
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
	    This function turns off a specified actuator for a specific greenhouse. 
	    It retrieves the actuator's tag path based on the greenhouse ID and actuator name, writes a 'False' value to the tag to turn off the actuator, and logs the action. 
	    If successful, it returns True; otherwise, it returns False.
	    """
	greenhouse = get_greenhouse_from_id(str(greenhouse_id))
	
	actuator_tag_path = greenhouse[actuator_name].tag_path
	
	if not greenhouse[actuator_name].get_value():
		return True
	
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
	    This function turns on a specified actuator for a specific greenhouse. 
	    It retrieves the actuator's tag path based on the greenhouse ID and actuator name, writes a 'True' value to the tag to turn on the actuator, and logs the action. 
	    If successful, it returns True; otherwise, it returns False.
	"""
	greenhouse = get_greenhouse_from_id(str(greenhouse_id))
	
	actuator_tag_path = greenhouse[actuator_name].tag_path
	
	if greenhouse[actuator_name].get_value():
		return True
	
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
        This function retrieves information about all greenhouses and formats it into a list of dictionaries. 
        Each dictionary contains a 'label' representing the greenhouse name and a 'value' representing the greenhouse ID. 
        It provides a convenient way to access and display information about all greenhouses within the system.
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
	    This function creates a new tag or overrides an existing tag at the specified path. 
	    It takes the tag's path, name, and value as arguments and determines the tag's data type based on the provided value. 
	    It then configures the tag with the specified attributes, including the data type, name, and value. 
	    If a tag already exists at the specified path, it will be overridden with the new configuration.
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


def greenhouse_auto_mode(greenhouse, greenhouse_id):
	"""
	Activates automatic mode for a greenhouse and manages its actuators based on the current preset.
	
	Args:
	    * greenhouse (dict): A dictionary containing greenhouse configuration data.
	    * greenhouse_id (int): The ID of the greenhouse.
	
	Returns:
	    None
	
	Notes:
	    This function enables automatic mode for a greenhouse by retrieving and managing its actuators based on the current preset.
	    It first determines the current preset ID for the greenhouse and fetches the corresponding preset. 
	    It then retrieves the current stage and manages each actuator's parameters using the `parameter_handler` function. 
	    This function is typically used to automate greenhouse operations based on predefined presets.
	"""
	current_preset_id = greenhouse['PresetId'].get_value()
	current_preset = get_preset_from_id(current_preset_id)
	stages = current_preset['Stages']
	current_stage = get_current_stage(stages)
	
	for actuator_name, actuator_stage in current_stage.items():
		if actuator_name in [ 'StartDate', 'EndDate' ]:
			continue
		parameter_handler(greenhouse, greenhouse_id, actuator_name, actuator_stage)


def get_auto_from_greenhouse(greenhouse_id):
	"""
	Retrieves the 'Auto' status of a greenhouse based on its ID.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse.
	
	Returns:
	    bool or int: The 'Auto' status of the greenhouse (True for auto mode, False for manual mode), or -1 if an error occurs.
	
	Notes:
	    This function retrieves the 'Auto' status of a greenhouse by reading the corresponding tag based on its unique ID. 
	    It returns a boolean value indicating whether the greenhouse is in auto mode (True) or manual mode (False). If an error occurs while reading the tag, it returns -1.
	"""
	base_path = '[default]GreenHouses/'
	tag_path = base_path + str(greenhouse_id) + '/Auto'
	try:
		return system.tag.readBlocking(tag_path)[0].value
	except:
		return -1


def get_preset_id_from_greenhouse(greenhouse_id):
	"""
	Retrieves the preset ID of a greenhouse based on its ID.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse.
	
	Returns:
	    int or -1: The preset ID associated with the greenhouse, or -1 if an error occurs.
	
	Notes:
	    This function retrieves the preset ID of a greenhouse by reading the corresponding tag based on its unique ID. 
	    It returns an integer representing the preset ID associated with the greenhouse. If an error occurs while reading the tag or the preset ID is not found, it returns -1.
	"""
	base_path = '[default]GreenHouses/'
	tag_path = base_path + str(greenhouse_id) + '/PresetId'
	try:
		return system.tag.readBlocking(tag_path)[0].value
	except:
		return -1


def greenhouses_auto_mode():
	"""
    Activates automatic mode for greenhouses.

    Returns:
        None

    Notes:
        This function enables automatic mode for greenhouses by iterating through all available greenhouses in the system.
        It checks the 'Auto' status for each greenhouse, and if it is set to True, it activates the automatic mode for that specific greenhouse by calling the 'greenhouse_auto_mode' function. 
        Automatic mode typically involves managing and controlling various environmental parameters and actuators within the greenhouse.
    """
	greenhouses = get_greenhouses()
	for greenhouse_id, greenhouse in greenhouses.items():
		auto_mode = greenhouse['Auto'].get_value()
		if auto_mode:
			greenhouse_auto_mode(greenhouse, greenhouse_id)

# PRESET FUNCTIONS

def set_auto(greenhouse_id, is_auto):
	"""
	Toggles on and off automatic mode for a greenhouse
	
	Args:
		* greenhouse_id (str): the ID of the greenhouse
		* is_auto (bool): True if auto mode is on, else False
	
	Returns:
		None
	"""
	
	greenhouse = get_greenhouse_from_id(greenhouse_id)
	path = greenhouse['Auto'].tag_path
	try:
		write_tag(path, is_auto)
		core.utils.logger.info('set_auto()', 'set auto mode to {} for greenhouse: {}'.format(is_auto, greenhouse_id))
	except:
		core.utils.logger.exc('set_auto()', traceback.format_exc())


def get_presets():
	"""
	Retrieves a list of formatted configuration presets.
	
	Returns:
	    dict: A dictionary containing configuration presets with their unique IDs as keys.
	
	Notes:
	    This function retrieves a dictionary of formatted configuration presets. 
	    It collects preset data from tags in the system and formats it as a dictionary, where each key represents a unique preset ID. 
	    This collection of presets can be used to manage and access configuration presets in the system.
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
        This function retrieves a configuration preset from the system based on its unique ID. 
        It takes the preset ID as an argument and returns a dictionary containing information about the specified preset. 
        If the preset ID is not found, an empty dictionary is returned.
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
        This function determines the current stage from a dictionary of stages by comparing the current date and time with the start and end dates of each stage. 
        It returns the current stage number or a dictionary with stage details if a current stage is found. If no current stage is found or an error occurs, it returns -1.
    """

	now = system.date.now()
	now_millis = system.date.toMillis(now)
	
	if len(stages.keys()) < 1:
		return -1
	
	for stage_number, stage in stages.items():
		try:
			if(now_millis >= system.date.toMillis(stage['StartDate'].get_value()) and now_millis < system.date.toMillis(stage['EndDate'].get_value())):
				return stage
		except:
			import traceback
			core.utils.logger.exc('get_current_stage', traceback.format_exc())
	
	return -1


def parameter_handler(greenhouse, greenhouse_id, actuator_name, actuator_stage):
	"""
	Manages actuator parameters based on the current stage of a greenhouse.
	
	Args:
	    * greenhouse (dict): A dictionary containing greenhouse configuration data.
	    * greenhouse_id (int): The ID of the greenhouse.
	    * actuator_name (str): The name of the actuator.
	    * actuator_stage (dict): A dictionary containing actuator stage parameters.
	
	Returns:
	    None
	
	Notes:
	    This function manages actuator parameters for a greenhouse based on the current stage of operation. It handles both temporized (timed) and setpoint-based actuators. 
	    If the actuator is temporized, it calculates a timed parameter change using `timed_parameter_handler`. 
	    If the actuator is setpoint-based, it sets the low and high setpoints using `setpoints_parameter_handler`. This function is a part of the automatic mode control for greenhouses.
	"""
	is_temp = actuator_stage.get('IsTemp').get_value()

	if is_temp:
		start_time = actuator_stage.get('StartTime').get_value()
		end_time = actuator_stage.get('EndTime').get_value()
		timed_parameter_handler(greenhouse_id, start_time, end_time, actuator_name)
	else:
		low_setpoint = actuator_stage.get('LowSetpoint').get_value()
		high_setpoint = actuator_stage.get('HighSetpoint').get_value()
		setpoints_parameter_handler(greenhouse, greenhouse_id, actuator_name, low_setpoint, high_setpoint)


def setpoints_parameter_handler(greenhouse, greenhouse_id, actuator_name, low_setpoint, high_setpoint):
	"""
	Handles actuator parameters based on setpoints for a greenhouse.
	
	Args:
	    * greenhouse (dict): A dictionary containing greenhouse configuration data.
	    * greenhouse_id (int): The ID of the greenhouse.
	    * actuator_name (str): The name of the actuator.
	    * low_setpoint (float): The lower setpoint for the actuator.
	    * high_setpoint (float): The higher setpoint for the actuator.
	
	Returns:
	    None
	
	Notes:
	    This function manages actuator parameters for a greenhouse based on setpoint values. 
	    It compares the current sensor value associated with the actuator to the specified low and high setpoints. 
	    If the sensor value is higher than the high setpoint, it turns off the actuator using the `turn_off` function. 
	    If the sensor value is lower than the low setpoint, it turns on the actuator using the `turn_on` function. 
	    This function is used to maintain environmental conditions within desired setpoint ranges in automatic mode.
	"""
	sensor_name = core.greenhouse.classes.SensorForActuator[actuator_name]
	sensor_value = greenhouse[sensor_name].get_value()
	
	if sensor_value > high_setpoint:
		turn_off(greenhouse_id, actuator_name)
	elif sensor_value < low_setpoint:
		turn_on(greenhouse_id, actuator_name)


def timed_parameter_handler(greenhouse_id, start_time, end_time, actuator_name):
	"""
	Handles timed parameters, turning on or off actuators if needed.
	
	Args:
		* greenhouse_id (int): the ID of the greenhouse involved.
		* start_date (date): The start date of the actuator's activation period.
		* end_date (date): The end date of the actuator's activation period.
		* actuator_name (str): The name of the actuator involved.
	
	Returns:
		None
	"""
	now = system.date.now()
	now_minute = system.date.getMinute(now)
	now_hour = system.date.getHour24(now)
	start_date_minute = system.date.getMinute(start_time)
	start_date_hour = system.date.getHour24(start_time)
	end_date_minute = system.date.getMinute(end_time)
	end_date_hour = system.date.getHour24(end_time)
	
	if now_hour > start_date_hour and now_hour < end_date_hour:
		turn_on(greenhouse_id, actuator_name)
	elif now_hour == start_date_hour or now_hour == end_date_hour:
		if now_minute >= start_date_minute and now_hour <= end_date_hour and now_minute < end_date_minute:
			turn_on(greenhouse_id, actuator_name)
	else:
		turn_off(greenhouse_id, actuator_name)


def get_new_preset_id():
	"""
    Retrieves and increments the current preset ID for configuration.

    Returns:
    	* str: A string representing the new preset ID.

    Notes:
        This function retrieves the current preset ID for configuration from a specified path. 
        It increments the current ID by 1 and writes the updated ID back to the same path.
        The new preset ID is returned as a string. This function is typically used to generate unique IDs for configuration presets.
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
	    This function takes a dictionary representing a configuration preset and saves it to tags in the system. 
	    It creates or overrides tags with preset data, including description, name, number of stages, stage details, and specific settings for ventilation, UV light, and irrigation pump for each stage. 
	    The function is typically used to store and manage configuration presets in the system.
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
	    This function is intended for GUI use and retrieves a list of formatted configuration presets.
	    It collects preset data from tags in the system and formats it into a list of dictionaries. 
	    Each dictionary contains information about a configuration preset, including its preset ID, name, and description. 
	    This list can be used to display and select presets within a graphical user interface.
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
	    This function deletes a configuration preset from the system based on its unique ID. 
	    It takes the preset ID as an argument and removes the corresponding tag associated with that preset from the system. 
	    After calling this function, the specified configuration preset will no longer be available in the system.
	"""
	presets_path = '[default]Presets'
	system.tag.deleteTags([presets_path + '/' + preset_id])


def set_preset_to_greenhouse(preset_id, greenhouse_id):
	"""
	Set a preset to a greenhouse.
	
	Args:
		* preset_id (str): the ID of the preset to assign
		* greenhouse_id (str): the ID of the greenhouse the preset is assigned to
	
	Returns:
		None
	"""
	
	greenhouse = get_greenhouse_from_id(greenhouse_id)
	path = greenhouse['PresetId'].tag_path
	try:
		write_tag(path, int(preset_id))
		core.utils.logger.info('assign_preset_to_greenhouse()', 'assigned preset {} to greenhouse: {}'.format(is_auto, greenhouse_id))
	except:
		import traceback
		core.utils.logger.exc('assign_preset_to_greenhouse()', traceback.format_exc())


def store_new_preset_to_db(preset_id):
	"""
	Stores a preset and all its stages into the database.
	
	Args:
		* preset_id (str): the ID of the preset to store.
	
	Returns:
		None
	"""
	
	preset = get_preset_from_id(preset_id)
	preset_name = preset.get('Name').get_value()
	description = preset.get('Description').get_value() 
	frwk.db.database.insert_new_preset(description, preset_name, preset_id)
	for stage_number in preset.get('Stages'):
		store_new_stage_to_db(stage_number, preset_id)


def store_new_stage_to_db(stage_number, preset_id):
	"""
	Stores a stage into the database.
	
	Args:
		* stage_number (str): the number of the stage to store.
		* preset_id (str): the ID of the stage's preset.
	
	Returns:
		None
	"""
	
	preset = get_preset_from_id(preset_id)
	stage = preset.get('Stages').get(str(stage_number))
	for parameter_name in stage:
		if parameter_name in [ 'StartDate', 'EndDate' ]:
			continue
		end_time = stage.get(parameter_name).get('EndTime').get_value()
		high_setpoint = stage.get(parameter_name).get('HighSetpoint').get_value()
		is_temp = stage.get(parameter_name).get('IsTemp').get_value()
		low_setpoint = stage.get(parameter_name).get('LowSetpoint').get_value()
		start_time = stage.get(parameter_name).get('StartTime').get_value()
		frwk.db.database.insert_new_stage(end_time, high_setpoint, is_temp, low_setpoint, parameter_name, preset_id, stage_number, start_time)
