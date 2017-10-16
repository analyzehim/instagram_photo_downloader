import requests
import shutil


def check_instagram(url):
    if "instagram" in url:
        return True
    return False


def transform(url):
    if url[-1] != '/':
        url += '/'
    return url + 'media/?size=l'


def download_file(url):
    local_filename = "images/" + url.split('/')[-3] + '.jpg'
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return local_filename
