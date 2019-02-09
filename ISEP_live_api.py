import requests
import json

# constants
co_url = 'https://iseplive.fr/connexion'
login_url = "https://iseplive.fr/api/auth"
base_url = 'https://iseplive.fr/api/media/gallery/{}/images'



# to fetch media only for the moment

class ISEP_live_account:
    def __init__(self, login='', password=''):
        self.headers = {}
        self.session = requests.session()
        self.session.headers = self.headers
        self._login = login
        self.password = password
        self.logged = False

    def login(self, verbose=False):
        self.session.get(co_url)
        r = self.session.post(
            login_url, json={'password': self.password, 'username': self._login})
        try :
            self.token = json.loads(r.text)['token']
        except :
            raise Exception('Login failed')
        self.headers['Authorization'] = 'Bearer ' + self.token
        self.headers['X-Refresh-Token'] = self.token
        self.logged = True
        if verbose:
            print('Logged in')

    def get_imgs_links(self, ide):
        url = base_url.format(ide)
        r = self.session.get(url)
        links = map(lambda x: 'https://iseplive.fr/api' +
                    x['fullSizeUrl'], json.loads(r.text))
        return links

    def get_json(self, url):
        return json.loads(self.session.get(url).text)

    def get_media_ids(self):
        if not self.logged :
            raise Exception('Not logged in')
        r = json.loads(self.session.get(
            'https://iseplive.fr/api/media?page=0').text)
        rangee = r['totalPages']
        page_range = [i for i in range(rangee)]
        ids = []
        for r in page_range:
            ids += list(map(lambda x: x['id'], self.get_json(
                'https://iseplive.fr/api/media?page={}'.format(r))['content']))
        return ids
