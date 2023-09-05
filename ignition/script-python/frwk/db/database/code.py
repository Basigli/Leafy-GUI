def log_input_sensors(greenhouse_id, air_hum, air_temp, light_quantity, terrain_hum, is_tank_empty):
	"""
	Saves input sensors data into the db

	Args:
		* greenhouse_id (int): id of the greenhouse
		* air_hum (float):
		* air_temp (float):
		* light_quantity (float):
		* terrain_hum (float):
		* is_tank_empty (bool): 
	Returns:
		True if the action is performed, False otherwise 
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
	Saves output actuators data into the db

	Args:
		* greenhouse_id (int): id of the greenhouse
		* irrigation_pump (bool):
		* uv_light (bool):
		* ventilation (bool):

	Returns:
		(bool) True if the action is performed, False otherwise 
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
	
	