import requests
import re
import shutil
import os


def check_instagram(url):
    instareg = re.compile('(https?:\/\/www\.)?instagram\.com(\/p\/[a-zA-Z0-9-_]+\/?)')
    if instareg.search(url) == None:
        return False
    return True


def transform(url):
    url = url.split('?')[0]
    if url[-1] != '/':
        url += '/'
    file_name = url.split('/')[-2] + '.jpg'       
    location_name = os.path.join("images", file_name)
    if os.name == 'nt': #real dirty hack to beatiful windows way writing path names
        location_name = "images//" + file_name
    return url + 'media/?size=l', location_name


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return True
