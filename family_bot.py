#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@family_harli_bot
Name - Family_bot

Description - A bot for telegrams, 
	which shows how many days have passed 
	since the significant date.

Author - Kharlamov Ilya
'''

from time import *
from datetime import *
import pytz
from mydata import *
from uuid import uuid4
import re
from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultArticle, ParseMode, \
	InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, \
	CallbackQueryHandler, JobQueue
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)


#Даты / Dates
tzmsk = pytz.timezone('Europe/Moscow') #GMT + 3 
wedding_date    = datetime(2015,10,17,16,0,  tzinfo =  tzmsk )
child_born_date = datetime(2017,10,30,16,24, tzinfo =  tzmsk)
first_date		= datetime(2010,3,14,19,0, tzinfo =  tzmsk)

def start(bot, update):
	"""Send a message when the command /start is issued."""
	name = update.message.from_user['first_name']
	text = 'Привет, '+ name + ', нажми /help, чтоб узнать список комманд'
	update.message.reply_text(text)
	

def help(bot, update):
	text = "Список комманд:\n /how - узнать сколько прошло дней с важных событий"
	update.message.reply_text(text)

def how(bot, update):
	today = datetime.now(tzmsk)
	text = "%s - прошло со дня свадьбы\n\n\
	%s - прошло со дня рождения дочери\n\n\
	%s - прошло со дня кражи сердца" % ((today - wedding_date), (today - child_born_date), (today - first_date))
	update.message.reply_text(text)

def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Такой команды здесь нет\nSorry, I didn't understand that command.")


def main():
	"""Start bot"""

	updater = Updater(family_harli_bot)

	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('help', help))
	dp.add_handler(CommandHandler('how', how))


	#это всегда должно быть в конце всех add_handler
	unknown_handler = MessageHandler(Filters.command, unknown)
	dp.add_handler(unknown_handler)

	# log all errors
	dp.add_error_handler(error)

	#start bot
	updater.start_polling(poll_interval = 1, timeout=600, allowed_updates = ['message'])

	updater.idle()

if __name__ == '__main__':
	print("############### Bot is run ###############")
	main()
