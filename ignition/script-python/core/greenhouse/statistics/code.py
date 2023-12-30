from core.utils.testing.decorator import *


#@timed
def day_avg(parameter_name, greenhouse_id, year, month, day):
	"""
	This function calculates the daily average of a parameter
	
	Args:
		*parameter_name (str): the name of the parameter
		*greenhouse_id (int): the ID of the greenhouse the preset is assigned to
		*year (int): the year of the date whose average is to be calculated
		*month (int): the month of said date
		*day (int): the day of the month of said date
		
	Returns:
		None
	"""
	start_date = system.date.getDate(year, month, day)
	end_date = system.date.getDate(year, month, day+1)
	system.date.addMillis(end_date, -1)
	if parameter_name in ['IrrigationPump', 'UVLight', 'Ventilation']:
		return day_avg_actuators(parameter_name, greenhouse_id, start_date, end_date)
	elif parameter_name in ['AirHumidity', 'AirTemperature', 'AirQuantity', 'TerrainHumidity']:
		return day_avg_sensors(parameter_name, greenhouse_id, start_date, end_date)
	else:
		core.utils.logger.err('core.greenhouse.statistics.day_avg', 'parameter not recognized')


def day_avg_sensors(parameter_name, greenhouse_id, start_date, end_date):
	"""
	Calculates the average value of a parameter collected by a sensor
	
	Args:
		*parameter_name (str): the name of the parameter
		*greenhouse_id (int): the ID of the greenhouse the preset is assigned to
		*start_date (datetime): midnight of the day whose average is to be calculated
		*end_date (datetime): 23:59:59.999 of said day
		
	Returns:
		The average value of the parameter
	"""
	params = {
		'greenHouseId':greenhouse_id,
		'startDate':start_date,
		'endDate':end_date
	}
	try:
		data = system.db.runNamedQuery('Select/GetSensorData', params)
	except:
		import traceback
		core.utils.logger.exc('core.greenhouse.statistics.day_avg_sensors', traceback.format_exc())
		return False
	column = core.greenhouse.classes.TagNamesToDB[parameter_name]
	values = [data.getValueAt(row, column) for row in range(data.getRowCount())]
	avg = system.math.mean(values)
	return avg


def day_avg_actuators(parameter_name, greenhouse_id, start_date, end_date):
	"""
	Calculates the activity percentage of a parameter handled by an actuator
	
	Args:
		*parameter_name (str): the name of the parameter
		*greenhouse_id (int): the ID of the greenhouse the preset is assigned to
		*start_date (datetime): midnight of the day whose average is to be calculated
		*end_date (datetime): 23:59:59.999 of said day
		
	Returns:
		The activity percentage of the actuator
	"""
	params = {
		'greenHouseId':greenhouse_id,
		'startDate':start_date,
		'endDate':end_date
	}
	try:
		data = system.db.runNamedQuery('Select/GetActuatorsData', params)
		data = system.dataset.toPyDataSet(data)
	except:
		import traceback
		core.utils.logger.exc('core.greenhouse.statistics.day_avg_actuators', traceback.format_exc())
		return False
	column = core.greenhouse.classes.TagNamesToDB[parameter_name]
	deltas = []
	start = None
	is_active = False
	for row in data:
		if row[column] == 1 and start is None:
			start = row['timeStamp']
			is_active = True
		elif row[column] == 0 and start is not None:
			end = row['timeStamp']
			deltas.append(system.date.millisBetween(start, end))
			start = None
			is_active = False
	if is_active:
		deltas.append(system.date.millisBetween(start, end_date))
	return system.math.sum(deltas)/86400000 