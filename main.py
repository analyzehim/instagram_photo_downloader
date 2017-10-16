# -*- coding: utf-8 -*-
import sys

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

    if cmd == '/help':
        telebot.send_text(from_id, 'No help today. Sorry, %s' % name)

    elif cmd == '/exit' and from_id == ADMIN_ID:
        # telebot.send_text_with_keyboard(from_id, 'Shut down?', [["Yes", "No"]])
        telebot.send_text(from_id, 'Finish by user {0} on {1}'.format(name, telebot.host))
        EXIT_MODE = True

    elif check_instagram(cmd):
        image_url = transform(cmd)
        name = download_file(image_url)
        telebot.send_photo(from_id, name)

    else:
        log_event('No action')


if __name__ == "__main__":
    telebot = Telegram()
    telebot.send_text(ADMIN_ID, "Run on {0}".format(telebot.host))
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
