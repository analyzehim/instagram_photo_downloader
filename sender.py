# -*- coding: utf-8 -*-
from bot_proto import Telegram
from log_proto import logDB

telebot = Telegram()
log = logDB()
text = '''No reason to panic - the bot is back in service!\n Нет причин для паники - бот снова в строю!'''

users_list = log.get_user_list()
for user in users_list:
    telebot.send_text(user, text)