import telebot
# from tg_bot_info import *

# Попробуйте ввести в Terminal вот это, если бот не включится:
# pip3 uninstall telebot
# pip3 uninstall PyTelegramBotAPI
# pip3 install pyTelegramBotAPI
# pip3 install --upgrade pyTelegramBotAPI


bot = telebot.TeleBot("5956003891:AAF9k0lCbhildThOwDj1BniNj84aSpUAwKQ")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)


bot.infinity_polling()

# import telebot
# from telebot import types
#
# keyboard1 = telebot.types.ReplyKeyboardMarkup()
# keyboard1.row('Ok', 'Bye')
#
# bot = telebot.TeleBot("5956003891:AAF9k0lCbhildThOwDj1BniNj84aSpUAwKQ")
#
#
# @bot.message_handler(commands=['start'])
# def start_message(message):
# 	bot.send_message(message.chat.id, 'Hi what do you want /start', reply_markup=keyboard1)
#
#
# @bot.message_handler(content_types=['text'])
# def send_text(message):
# 	if message.text.lower() == 'Hello':
# 		bot.send_message(message.chat.id, message.text.upper())
# 	elif message.text.lower() == 'Bye':
# 		bot.send_message(message.chat.id, 'see you soon')
# 	elif message.text.lower() == 'I love you':
# 		bot.send_sticker(message.chat.id, 'API')
#
#
# @bot.message_handler(content_types=['sticker'])
# def sticker_id(message):
# 	print(message)
#
#
# bot.polling(none_stop=True)
