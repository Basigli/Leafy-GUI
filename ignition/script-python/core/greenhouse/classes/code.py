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
