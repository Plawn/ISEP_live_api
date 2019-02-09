from multi_downloader import Download_pool
import Fancy_downloader as dl
import json
import os
from ISEP_live_api import ISEP_live_account
import requests
import shutil


input_folder = 'profiles'
output_folder = 'loaded_profiles'


def fetch_profile(filename, session):
    with open(filename, 'r') as f:
        content = json.load(f)
    old_filename = filename
    filename = '.'.join(filename.split('/')[-1].split('.')[:-1])
    path = os.path.join(output_folder, filename)
    try :
        os.mkdir(path)
        shutil.copy(old_filename, os.path.join(path, 'info.json'))
    except:
        print('skipped creating folder')
    if content['photoUrl'] is not None:
        photo_url = 'https://iseplive.fr/api/' + content['photoUrl']
        session.headers['Accept'] = 'image/webp,image/apng,image/*,*/*;q=0.8'
        session.headers['Accept-Encoding'] = 'gzip, deflate, br'
        session.headers['Accept-Language'] = 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        session.headers['Connection'] = 'keep-alive'
        session.headers['DNT'] = '1'
        session.headers['Cache-Control'] = 'no-cache'
        session.headers['Host'] = 'iseplive.fr'
        session.headers['Pragma'] = 'no-cache'
        session.headers['Referer'] = 'https://iseplive.fr/accueil'
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

        d = dl.Download(url=photo_url, filename='profile_pic.jpg',
                        type='basic', session=session)
        d.set_download_folder(path)
        return d


if __name__ == '__main__':
    user = ISEP_live_account('pale60442', 'WL$K2mPp')
    user.login()
    downloads = map(lambda x: fetch_profile(x, user.session), map(
        lambda x: os.path.join(input_folder, x), os.listdir(input_folder)))
    pool = Download_pool(10)
    pool.start()
    for download in filter(lambda x: x != None, downloads):
        pool.add(download, True)
    pool.stop_finished()
