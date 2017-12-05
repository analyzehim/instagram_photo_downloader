from bot_proto import *
from log_proto import *
import datetime

if __name__ == "__main__":

    while True:
        telebot = Telegram()
        log = logDB()
        try:
            if datetime.datetime.now().hour == 24:
                telebot.send_text(telebot.admin_id, "{0} unique users in the last 24 hours".format(log.get_status(24)))
                time.sleep(60 * 60)

        except KeyboardInterrupt:
            print 'Interrupt by user..'
            break

        except Exception, e:
            log_event(get_exception())
