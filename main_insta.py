# -*- coding: utf-8 -*-
from bot_proto import *
from instagram_proto import *
from log_proto import *
from multiprocessing.dummy import Pool as ThreadPool

EXIT_MODE = False


def check_updates():
    parameters_list = telebot.get_updates()

    if EXIT_MODE:
        return 1
    if not parameters_list:
        return 0
    pool = ThreadPool(8)
    results = pool.map(run_command, parameters_list)
    print results
    pool.close()
    pool.join()
    for parameter in parameters_list:
        log.add_message(*parameter)





def run_command(parametrs):
    (name, from_id, cmd, author_id, date) = parametrs
    global EXIT_MODE
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
        return(name, from_id, date, file_name)

    else:
        telebot.send_text(from_id, 'Send the correct link to Instagram post, like https://www.instagram.com/p/BeOJzBCDyuD/?taken-by=instagram')
        log_event('No action')


if __name__ == "__main__":

    telebot = Telegram()
    log = logDB()
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
            log_event(get_exception())
