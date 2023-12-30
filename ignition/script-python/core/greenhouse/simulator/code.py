"""
For testing only!
"""
import random
NORMAL_RATE = 0.4


def simulator():
	greenhouses = core.greenhouse.controller.get_greenhouses()
	
	for greenhouse_id, greenhouse in greenhouses.items():
		terrain_humidity_sim(greenhouse_id)


def terrain_humidity_sim(greenhouse_id):
	base_path = '[default]GreenHouses/'
	greenhouse_path = base_path + str(greenhouse_id)
	tag_path = greenhouse_path + '/TerrainHumidity'

	normal_rate = - (NORMAL_RATE + random.random())
	irrigation_rate = 1
	
	try:
		value = system.tag.readBlocking(tag_path)[0].value
		irrigation_is_active = system.tag.readBlocking(greenhouse_path + '/IrrigationPump')[0].value
		if value <= 0 and not irrigation_is_active:
			value = 0
		else:
			value = value + (irrigation_rate if irrigation_is_active else normal_rate)
		system.tag.writeBlocking(tag_path, [value])
	except:
		pass


def air_humidity_sim(greenhouse_id):
	base_path = '[default]GreenHouses/'
	greenhouse_path = base_path + str(greenhouse_id)
	tag_path = greenhouse_path + '/AirHumidity'
	
	descent_rate = - (NORMAL_RATE + random.random())
	ascent_rate = (NORMAL_RATE + random.random())
	
	try:
		value = system.tag.readBlocking(tag_path)[0].value
		# value = value + 
		system.tag.writeBlocking(tag_path, [value])
	except:
		pass
