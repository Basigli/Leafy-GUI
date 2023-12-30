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
	def __init__(self, name, value, ):
		self.name = name
		self.value = value


class Greenhouse():
	def __init__(self, id, name):
		self.id = id
		self.name = name
	
	def to_payload(self):
		return {'id': self.id, 'name': self.name}