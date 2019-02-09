import requests
import os

# to upload photos to the server

dire = '13442'
url = 'https://home.plawn-inc.science/face/upload'
password = 'leubzezeh97869UYVD'

def upload_one_pic(directory, filename):
    files = {'file': open(os.path.join(directory, filename), 'rb')}
    res = requests.post(url, files=files, data={'password': password})
    print(res.text)

for filename in os.listdir('13442'):
    upload_one_pic(dire, filename)
    print(filename)
