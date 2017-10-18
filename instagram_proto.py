import requests
import shutil
import os

def check_instagram(url):
    if "instagram" in url:
        return True
    return False


def transform(url):
    url = url.split('?')[0]
    if url[-1] != '/':
        url += '/'
    file_name = url.split('/')[-2] + '.jpg'       
    location_name = os.path.join("images", file_name)
    return url + 'media/?size=l', location_name


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return True
