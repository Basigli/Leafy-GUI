import telegram

bot = telegram.Bot(token='6764961036:AAE4iNNf622I8wyTSqbAsARR7F8z5Nn83AE')


#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#    """Send a message when the command /start is issued."""
#    user = update.effective_user
#    await update.message.reply_html(
#        rf"Hi {user.mention_html()}!",
#        reply_markup=ForceReply(selective=True),
#    ) DA SISTEMARE

def tank_empty_alert(greenhouse_id):
	message = bot.getUpdates()[-1].message
	chat_id = message.chat_id
	print("Type: %s, Value: %s " % (type(chat_id), chat_id))
	print("Type: %s, Value: %s " % (type(message), message))
	text = "Greenhouse %s: The tank is empty. Irrigation has been paused. Refill the tank to resume operation" % greenhouse_id
	bot.sendMessage(chat_id=chat_id, text=text)
	



