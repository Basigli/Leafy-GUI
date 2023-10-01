def log_input_sensors(greenhouse_id, air_hum, air_temp, light_quantity, terrain_hum, is_tank_empty):
	"""
	Saves input sensor data into the database.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse where the sensor data is recorded.
	    * air_hum (float): The air humidity value.
	    * air_temp (float): The air temperature value.
	    * light_quantity (float): The quantity of light in the greenhouse.
	    * terrain_hum (float): The humidity of the terrain in the greenhouse.
	    * is_tank_empty (bool): A boolean indicating whether the tank is empty or not.
	
	Returns:
	    bool: True if the action is successfully performed and the sensor data is saved in the database, False otherwise.
	
	Notes:
	    This function records sensor data into the database for a specific greenhouse. It takes various sensor readings as input and stores them along with a timestamp in the database. If the data recording is successful, the function returns True. If there is an error during the database operation, it logs the error and returns False.
	"""
	
	params = {
		'airHum': air_hum,
		'airTemp': air_temp,
		'greenHouseId': greenhouse_id,
		'isTankEmpty': is_tank_empty,
		'lightQuantity': light_quantity,
		'terrainHum': terrain_hum,
		'timeStamp': system.date.now()
	}
	
	try:
		system.db.runNamedQuery('InsertIntoINPUT_SENSORS', params)
		return True
	except:
		import traceback
		core.utils.logger.exc('log_input_sensors', traceback.format_exc())
		return False
		
		
def log_output_actuators(greenhouse_id, irrigation_pump, uv_light, ventilation):
	"""
	Saves output actuator data into the database.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse where the actuator data is recorded.
	    * irrigation_pump (bool): A boolean indicating the status of the irrigation pump (True for on, False for off).
	    * uv_light (bool): A boolean indicating the status of UV lights (True for on, False for off).
	    * ventilation (bool): A boolean indicating the status of ventilation (True for on, False for off).
	
	Returns:
	    bool: True if the action is successfully performed, False otherwise.
	
	Notes:
	    This function records actuator data into the database for a specific greenhouse. It takes the status of various actuators as input and stores them along with a timestamp in the database. If the data recording is successful, the function returns True. If there is an error during the database operation, it logs the error and returns False.
	"""
	params = {
		'greenHouseId': greenhouse_id,
		'irrigationPump': irrigation_pump,
		'UVLight': uv_light,
		'ventilation': ventilation,
		'timeStamp': system.date.now()
	}
	try:
		system.db.runNamedQuery('InsertIntoOUTPUT_ACTUATORS', params)
		return True
	except:
		import traceback
		core.utils.logger.exc('log_input_sensors', traceback.format_exc())
		return False
	

def get_sensors_data(greenhouse_id, start_date, end_date):
	"""
	Retrieves sensor data from the database for a specified greenhouse within a given date range.
	
	Args:
	    * greenhouse_id (int): The ID of the greenhouse for which sensor data is requested.
	    * start_date (str): The start date of the data retrieval period (in string format).
	    * end_date (str): The end date of the data retrieval period (in string format).
	
	Returns:
	    list or None: A list of sensor data records as PyDataSet, or None if an error occurs during data retrieval.
	
	Notes:
	    This function retrieves sensor data from the database for a specific greenhouse within the specified date range. It returns the data as a list of records in PyDataSet format. If an error occurs during data retrieval, it logs the error and returns None.
	"""
	params = {
		'greenHouseId': greenhouse_id,
		'startDate': start_date,
		'endDate': end_date
	}
	try:
		return system.dataset.toPyDataSet(system.db.runNamedQuery('Select/GetSensorData', params))
	except:
		import traceback
		core.utils.logger.exc('log_input_sensors', traceback.format_exc())
		return 
	
	
def get_actuators_data(greenhouse_id, start_date, end_date):
	"""
    Retrieves actuator data from the database for a specified greenhouse within a given date range.

    Args:
        * greenhouse_id (int): The ID of the greenhouse for which actuator data is requested.
        * start_date (str): The start date of the data retrieval period (in string format).
        * end_date (str): The end date of the data retrieval period (in string format).

    Returns:
        list or None: A list of actuator data records as PyDataSet, or None if an error occurs during data retrieval.

    Notes:
        This function retrieves actuator data from the database for a specific greenhouse within the specified date range. It returns the data as a list of records in PyDataSet format. If an error occurs during data retrieval, it logs the error and returns None.
    """
	params = {
		'greenHouseId': greenhouse_id,
		'startDate': start_date,
		'endDate': end_date
	}	
	try:
		return system.dataset.toPyDataSet(system.db.runNamedQuery('Select/GetActuatorsData', params))
	except:
		import traceback
		core.utils.logger.exc('log_input_sensors', traceback.format_exc())
		return 
	

def insert_new_preset(description, preset_name, preset_id):
	return 
	
	
def insert_new_stage(end_date, high_setpoint, is_temp, low_setpoint, parameter_name, preset_id, stage_number, start_date):
	return 