from ISEP_live_api import ISEP_live_account
import os
import json
directory_out = 'profiles'


if __name__ == '__main__':
    account = ISEP_live_account('pale60442', 'WL$K2mPp')
    account.login()
    students = account.load_annuaire()
    for student in students :
        with open(os.path.join(directory_out, student['firstname']+'_'+student['lastname']+'.json'), 'w') as f:
            json.dump(student, f, indent=4)