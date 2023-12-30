it = {
	'@ui.params.terrainHum@':'Umidità Terreno',
	'@ui.text.history@':'Storico',
	'@ui.text.stages@':'Stadi di Crescita',
	'@ui.params.airHum@':'Umidità Aria',
	'@ui.text.name@':'Nome',
	'@ui.params.airTemp@':'Temperatura Aria',
	'@ui.state.notActive@':'Non Attiva',
	'@ui.text.stage@':'Stadio',
	'@ui.text.save@':'Salva',
	'@ui.params.lightQuantity@':'Livello Luminosità',
	'@ui.mode.manual@':'Manuale',
	'@ui.mode.auto@':'Auto',
	'@ui.state.full@':'Pieno',
	'@ui.text.presetSuccess@':'Preset Caricato Correttamente',
	'@ui.text.modify@':'Modifica',
	'@ui.text.greenhouse@':'Serra',
	'@ui.params.irrigationPump@':'Pompa Irrigazione',
	'@ui.text.presetError@':'Errore\!',
	'@ui.header.configure\ @':'Configura',
	'@ui.state.empty@':'Vuoto',
	'@ui.text.timePicker@':'Seleziona un Range Temporale',
	'@ui.params.tank@':'Livello Serbatoio',
	'@ui.text.pupup.success@':'Preset creato\!',
	'@ui.text.mode@':'Modalità',
	'@ui.state.active@':'Attiva',
	'@ui.text.description@':'Descrizione',
	'@ui.params.UVLight@':'Illuminazione UV',
	'@ui.params.ventilation@':'VEntilazione',
	'@ui.text.selectPreset@':'Seleziona Preset',
	'@ui.error.presetName@':'Esiste già un preset con questo nome'
}

en = {
	'@ui.params.terrainHum@':'Terrain Humidity',
	'@ui.text.history@':'History',
	'@ui.text.stages@':'Growth Stages',
	'@ui.params.airHum@':'Air Humidity',
	'@ui.text.name@':'Name',
	'@ui.params.airTemp@':'Air Temperature',
	'@ui.state.notActive@':'Not Active',
	'@ui.text.stage@':'Stage',
	'@ui.text.save@':'Save',
	'@ui.params.lightQuantity@':'Light Quantity',
	'@ui.mode.manual@':'Manual',
	'@ui.mode.auto@':'Auto',
	'@ui.state.full@':'Full',
	'@ui.text.presetSuccess@':'Preset Loaded Successfully',
	'@ui.text.modify@':'Modify',
	'@ui.text.greenhouse@':'Greenhouse',
	'@ui.params.irrigationPump@':'Irrigation Pump',
	'@ui.text.presetError@':'Error\!',
	'@ui.header.configure\ @':'Configure',
	'@ui.state.empty@':'Empty',
	'@ui.text.timePicker@':'Pickup Time Range',
	'@ui.params.tank@':'Tank level',
	'@ui.text.pupup.success@':'Preset created\!',
	'@ui.text.mode@':'Mode',
	'@ui.state.active@':'Active',
	'@ui.text.description@':'Description',
	'@ui.params.UVLight@':'UV Light',
	'@ui.params.ventilation@':'Ventilation',
	'@ui.text.selectPreset@':'Select Preset',
	'@ui.error.presetName@':'A preset with this name is already in use'
}

languages = {
	'it-IT':it,
	'it':it,
	'IT':it,
	'en-EN':en,
	'en':en,
	'EN':en
}

# esempio di utilizzo:
# translate('@ui.text.hello@', 'it-IT') -> 'Hello'
# TO DO:
# [] creare un dizionario con chiave 'term' e valore la traduzione in italiano
# [] creare un dizionario con chiave 'term' e valore la traduzione in inglese
# -----------------------------------------------------------------------------
# la funzione translate in base al 'locale' passato come argomento dovrà scegliere il giusto dizionario e restituire il termine tradotto
# Nota: crere i due dizionari come variabili globali, non all'interno della funzione

def translate(term, locale):
	"""
	This function translates the term into the locale language.
	
	Args:
		*term (str): the term to translate
		*locale (str): the client's language

	Returns:
		str: the term translated into the locale language
	"""
	try:
		language = languages[locale]
		return language[term]
	except:
		core.utils.logger.exc('core.utils.translations.translate', 'Term ' + term + ' not found!')
		return ''

