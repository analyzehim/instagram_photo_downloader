import requests
import shutil
import os

def check_instagram(url):
    if "instagram" in url:
        return True
    return False


def transform(url):
    if os.name =='posix':
        delimeter = '\\'
    elif os.name == 'nt':
        delimeter = '/'
    if url[-1] != '/':
        url += '/'
    return url + 'media/?size=l', "images{0}".format(delimeter) + url.split('/')[-2] + '.jpg'


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return True
