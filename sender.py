# -*- coding: utf-8 -*-
from bot_proto import Telegram
from log_proto import logDB

telebot = Telegram()
log = logDB()
text = '''The bot is back in service!\n Мужчина снова в строю!'''

users_list = log.get_user_list()
for user in users_list:
    telebot.send_text(telebot.admin_id, text)