import Fancy_downloader as dl
from multi_downloader import Download_pool, Download_worker
from ISEP_live_api import ISEP_live_account
import sys
import os
import shutil

def fetch_img_from_id(account, id):
    nb_workers = 10
    links = account.get_imgs_links(ide)
    try :
        shutil.rmtree(ide)
    except :
        print('folder already existing => starting anyway')
    os.mkdir(ide)

    pool = Download_pool(nb_workers=nb_workers, folder=ide)
    pool.start()
    for i, url in enumerate(links):
        pool.add(dl.Download(url=url, filename='{}.jpg'.format(i), type='basic'))

    pool.stop_finished()
    print('Download done')
    print('downloaded {} images'.format(i+1))

if __name__ == '__main__':
    ids = sys.argv[1:]
    user = ISEP_live_account() #login not required when downloading images
    # user.login()
    for ide in ids :
        fetch_img_from_id(user, ide)
