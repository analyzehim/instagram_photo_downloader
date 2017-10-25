# -*- coding: utf-8 -*-
import sys
import os
from bot_proto import *
from instagram_proto import *

EXIT_MODE = False


def check_updates():
    parameters_list = telebot.get_updates()

    if EXIT_MODE:
        return 1
    if not parameters_list:
        return 0
    for parameters in parameters_list:
        run_command(*parameters)


def run_command(name, from_id, cmd, author_id, date):
    global EXIT_MODE
    print telebot.admin_id, from_id
    if cmd == '/help':
        telebot.send_text(from_id, 'No help today. Sorry, %s' % name)
        
    elif cmd == '/start':
        telebot.send_text(from_id, 'Hello %s! Just send me a link to Instagram post' % name)
        
    elif cmd == '/exit' and from_id == telebot.admin_id:
        telebot.send_text(from_id, 'Finish by user {0} on {1}'.format(name, telebot.host))
        EXIT_MODE = True

    elif check_instagram(cmd):
        image_url, file_name = transform(cmd)
        if not os.path.isfile(file_name):
            download_file(image_url, file_name)
            log_event("{0} file is new".format(file_name))
        telebot.send_photo(from_id, file_name)

    else:
        log_event('No action')


if __name__ == "__main__":
    telebot = Telegram()
    telebot.send_text(telebot.admin_id, "Run on {0}".format(telebot.host))
    while True:
        try:
            if check_updates() != 1:
                time.sleep(telebot.Interval)
            else:
                sys.exit()
        except KeyboardInterrupt:
            print 'Interrupt by user..'
            break
        except Exception, e:
            log_event(str(e))
