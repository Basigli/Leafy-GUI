WINDOW_ID = "MessageWindow"

def message_success(text):
	"""
	Displays a new dock with a success message
	Can be called only by the perspective
	"""
	parameters = {
		"messageType": "S",
		"messageText": text
	}
	try:
		system.perspective.openDock(WINDOW_ID, params=parameters)
	except:
		import traceback
		core.utils.logger.exc("core.utils.gui.messages.message_success", traceback.format_exc())


def message_error(text):
	"""
	Displays a new dock with a error message
	Can be called only by the perspective
	"""
	parameters = {
		"messageType": "E",
		"messageText": text
	}
	try:
		system.perspective.openDock(WINDOW_ID, params=parameters)
	except:
		import traceback
		core.utils.logger.exc("core.utils.gui.messages.message_error", traceback.format_exc())


def message_info(text):
	"""
	Displays a new dock with an information message
	Can be called only by the perspective
	"""
	parameters = {
		"messageType": "I",
		"messageText": text
	}
	try:
		system.perspective.openDock(WINDOW_ID, params=parameters)
	except:
		import traceback
		core.utils.logger.exc("core.utils.gui.messages.message_info", traceback.format_exc())