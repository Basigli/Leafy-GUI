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
	    This function manages actuator parameters for a greenhouse based on the current stage of operation. It handles both temporized (timed) and setpoint-based actuators. If the actuator is temporized, it calculates a timed parameter change using `timed_parameter_handler`. If the actuator is setpoint-based, it sets the low and high setpoints using `setpoints_parameter_handler`. This function is a part of the automatic mode control for greenhouses.
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
	    This function manages actuator parameters for a greenhouse based on setpoint values. It compares the current sensor value associated with the actuator to the specified low and high setpoints. If the sensor value is higher than the high setpoint, it turns off the actuator using the `turn_off` function. If the sensor value is lower than the low setpoint, it turns on the actuator using the `turn_on` function. This function is used to maintain environmental conditions within desired setpoint ranges in automatic mode.
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
	start_date_minute = system.date.getMinute(start_date)
	start_date_hour = system.date.getHour24(start_date)
	end_date_minute = system.date.getMinute(end_date)
	end_date_hour = system.date.getHour24(end_date)
	
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


def assign_preset_to_greenhouse(preset_id, greenhouse_id):
	"""
	Assigns a preset to a greenhouse.
	
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
		core.utils.logger.exc('assign_preset_to_greenhouse()', traceback.format_exc())

def get_presets_as_list():
	"""
	Args:
		None
	Returns:
		A list of all saved preset's names.
	"""
	return [preset['name'] for preset in core.greenhouse.controller.get_formatted_presets_list()]