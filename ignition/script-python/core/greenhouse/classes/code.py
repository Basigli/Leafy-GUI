GREENHOUSE_BASE_PATH = '[default]GreenHouses'
ACTUATORS_RELATIVE_PATH = '/Actuators'
SENSORS_RELATIVE_PATH = '/Sensors'
INFO_RELATIVE_PATH = '/Info'


def get_actuators_path(greenhouse_id):
	return GREENHOUSE_BASE_PATH + '/%s'%(greenhouse_id) + ACTUATORS_RELATIVE_PATH


def get_sensors_path(greenhouse_id):
	return GREENHOUSE_BASE_PATH + '/%s'%(greenhouse_id) + SENSORS_RELATIVE_PATH



class Actuators():
	IRRIGATION = 'IrrigationPump'
	UV_LIGHT = 'UVLight'
	VENTILATION = 'Ventilation'


class Sensors():
	AIR_HUM = 'AirHumidity'
	AIR_TEMP = 'AirTemperature'
	IS_TANK_EMPTY = 'IsTankEmpty'
	LIGHT_QUANTITY = 'LightQuantity'
	TERRAIN_HUM = 'TerrainHumidity'


class MeasureUnit():
	CELSIUS = '°C'
	PERC = '%'

MeasureUnitForSensor = {
	Sensors.AIR_HUM: MeasureUnit.PERC,
	Sensors.AIR_TEMP: MeasureUnit.CELSIUS,
	Sensors.IS_TANK_EMPTY: None,
	Sensors.LIGHT_QUANTITY: MeasureUnit.PERC,
	Sensors.TERRAIN_HUM: MeasureUnit.PERC
}


SensorForActuator = {
	Actuators.IRRIGATION: Sensors.TERRAIN_HUM,
	Actuators.UV_LIGHT: Sensors.LIGHT_QUANTITY,
	Actuators.VENTILATION: Sensors.AIR_TEMP,
}


DBToTagNames = {
	'airHum': Sensors.AIR_HUM,
	'airTemp': Sensors.AIR_TEMP,
	'irrigationPump': Actuators.IRRIGATION,
	'isTankEmpty': Sensors.IS_TANK_EMPTY,
	'lightQuantity': Sensors.LIGHT_QUANTITY,
	'terrainHum': Sensors.TERRAIN_HUM,
	'UVLight': Actuators.UV_LIGHT,
	'ventilation': Actuators.VENTILATION
}


TagNamesToDB = {
	Sensors.AIR_HUM: 'airHum',
	Sensors.AIR_TEMP: 'airTemp',
	Actuators.IRRIGATION: 'irrigationPump',
	Sensors.IS_TANK_EMPTY: 'isTankEmpty',
	Sensors.LIGHT_QUANTITY: 'lightQuantity',
	Sensors.TERRAIN_HUM: 'terrainHum',
	Actuators.UV_LIGHT: 'UVLight',
	Actuators.VENTILATION: 'ventilation'
}


class Parameter():
	def __init__(self, name, value, measure_unit):
		self.name = name
		self.value = value
		self.measure_unit = measure_unit



class Greenhouse():
	def __init__(self, id):
		self.id = id
		self.name = system.tag.readBlocking(tagPaths)[0].getValue()
