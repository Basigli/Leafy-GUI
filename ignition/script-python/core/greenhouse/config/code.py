def create_new_greenhouse_instance(arduino_id, greenhouse_name):
	params =  {
		"ArduinoId" : arduino_id,
		"GreenhouseName": greenhouse_name
		}

	config = {
		"name": "3",       # da capire come ottenere un id univoco
		"typeId" : "Greenhouse",
		"tagType" : "UdtInstance",
		"parameters" : params
	}

	system.tag.configure(core.greenhouse.classes.GREENHOUSE_BASE_PATH, config)