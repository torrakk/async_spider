import os
from webcrawler.settings import *

RACINE='https://guichet-adresse.ign.fr'

URLS={'login':{'path':'login', 'parse_kwargs':('_csrf_token', '')},
      'ajouter une zone': {'path':'gcms/zone/add', 'parse_kwargs':{}},
      'export d\'une zone' :{}
     }

class guichetAdrrInteract():

    def __init__(self):
        self.codes = CODES.update({'_submit':'Connexion', '_csrf_token':'Csrf_Token'})

    def getobjmanq(self):


    def connexion(self):
        with closing(asyncio.get_event_loop()) as loop:
            con = Connect(scenario=[{'action': 'post_request', 'url': GUICHET_ADRESSE, 'data': CODES, 'nested': ''},
                                    {'action': 'get_request', 'url': GUICHET_ADRESSE}])
            loop.run_until_complete(con.do_scenari())

    def parse_page(self):
        '''
        Permet d'analyser la page comprennant les exports existants paramétrés
        :return: 
        '''
        kwargs = {'url': self.adresse, 'data': self.code}
        if 'Extraire' in self.resp:
            print('OK\n\n')

    def export_result(self):
        '''

        :return: 
        '''