from ISEP_live_api import ISEP_live_account
import sys
import os


if __name__ == '__main__':
    login, password = sys.argv[1], sys.argv[2]
    is_full = False
    if len(sys.argv) > 3 :
        if sys.argv[3] == 'full' :
            is_full= True
    user = ISEP_live_account(login, password)
    user.login()
    ids = user.get_media_ids()
    res = ' '.join(map(lambda x: str(x), ids))
    print(res)
    if is_full :
        os.system('python3 fetch_isep_live.py {}'.format(res))    
