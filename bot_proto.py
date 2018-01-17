# -*- coding: utf-8 -*-
import requests
import time
import socket
import sys
import traceback
import xml.etree.ElementTree as ET
import os

URL = 'https://api.telegram.org/bot'  # HTTP Bot API URL
INTERVAL = 0.5


def get_token(tree):
    root = tree.getroot()
    token = root.findall('token')[0].text
    return token


def get_admin(tree):
    root = tree.getroot()
    admin_id = root.findall('admin_id')[0].text
    return int(admin_id)


def get_proxies(tree):
    root = tree.getroot()
    proxy_url = root.findall('proxy')[0].text
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    return proxies


def check_mode(tree):
    import requests

    try:
        requests.get('https://www.google.com')
        return False
    except:
        proxies = get_proxies(tree)
        requests.get('https://www.google.com', proxies=proxies)
        return True


class Telegram:
    def __init__(self):
        if not os.path.exists("images"):
            os.makedirs("images")
        self.cfgtree = ET.parse('private_config.xml')
        self.proxy = check_mode(self.cfgtree)
        self.TOKEN = get_token(self.cfgtree)
        self.URL = 'https://api.telegram.org/bot'
        self.admin_id = get_admin(self.cfgtree)
        self.offset = 0
        self.host = socket.getfqdn()
        self.Interval = INTERVAL
        if self.proxy:
            self.proxies = get_proxies(self.cfgtree)
            log_event("Init completed with proxy, host: " + str(self.host))
        else:
            log_event("Init completed, host: " + str(self.host))

    def get_updates(self):
        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data, proxies=self.proxies)
        else:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data)
        if (not request.status_code == 200) or (not request.json()['ok']):
            return False

        if not request.json()['result']:
            return
        updates_list = []
        for update in request.json()['result']:
            self.offset = update['update_id']

            if 'message' not in update or 'text' not in update['message']:
                continue

            from_id = update['message']['chat']['id']  # Chat ID
            author_id = update['message']['from']['id']  # Creator ID
            message = update['message']['text'].encode("utf-8")
            date = update['message']['date']
            try:
                name = update['message']['chat']['first_name'].encode("utf-8")
            except:
                name = update['message']['from']['first_name'].encode("utf-8")
            parameters = (name, from_id, message, author_id, date)
            updates_list.append(parameters)
            log_event('from %s (id%s): "%s" with author: %s; time:%s' % parameters)
        return updates_list

    def send_text_with_keyboard(self, chat_id, text, keyboard):
        log_event('Sending to %s: %s; keyboard: %s' % (chat_id, text, keyboard))  # Logging
        json_data = {"chat_id": chat_id, "text": text,
                     "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True}}
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy
        else: # no proxy
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request
        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def send_photo(self, chat_id, imagePath):
        log_event('Sending photo to %s: %s' % (chat_id, imagePath))  # Logging
        data = {'chat_id': chat_id}
        files = {'photo': (imagePath, open(imagePath, "rb"))}
        requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files)
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files,
                                    proxies=self.proxies)  # HTTP request with proxy)                            
        else:
            request = requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files)  # HTTP request
        if not request.status_code == 200:  # Check server status
            return False

        return request.json()['ok']  # Check API

    def send_text(self, chat_id, text):
        log_event('Sending to %s: %s' % (chat_id, text))  # Logging
        data = {'chat_id': chat_id, 'text': text}  # Request create
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy
        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API


def log_event(text):
    f = open('log.txt', 'a')
    event = '%s >> %s' % (time.ctime(), text)
    print event + '\n'
    f.write(event + '\n')
    f.close()
    return


def get_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return ''.join('!! ' + line for line in lines)
