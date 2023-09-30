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