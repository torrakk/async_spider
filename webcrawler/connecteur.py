import re
import aiohttp
import asyncio
from contextlib import closing
import socket
import random

from webcrawler.settings import *
from webcrawler.exception import *
from webcrawler.utils import validateUrl

class Connect(object):
    # Variable permettant de partager les sessions en fonction des urls visitées et les fermer proprement /
    # une fois que ces dernières ont été visitées
    session_pool = {}

    def __init__(self, **scenari):
        '''
        L'objet connect permet de se connecter au guichet adresse et d'interrragir avec ce dernier
        :param adresse: adresse à laquelle se connecter (chaine de caractère)
        :param credentials: login et mdp contenues dans un dictionnaire
        '''
        #self.session = session
        self.scenari = scenari
        self.action, self.session = (self.scenari.pop(keys) for keys in ('action', 'session'))
        # si une session existe quelque part nous la prennons
        if not self.session:
            self.session = self.session_pool[self.scenari['url']] if self.scenari['url'] in self.session_pool.keys() \
                else self.scenari.pop('session', None) or None


    def testUrl(self, url):
        if not validateUrl(url):
            print(url)
            #print('Votre url est malformée')
            raise testUrlError('Votre url est malformée')

    async def _request(self, **kwargs):
        '''
        
        :param url: page demandée
        :return: 
        '''

        self.testUrl(kwargs['url'])
        print('url visitée :', kwargs['url'])
        try:

            async with self.session.__getattribute__(self.action)(**kwargs) as response:
                assert response.status == 200
                return (self.session, await response.text())
        except (aiohttp.client_exceptions.ClientResponseError, aiohttp.client_exceptions.ClientConnectorError, socket.gaierror) as e:
            print('Nous avons un problèmes de connexion au site --> {}'.format(e))

    async def request(self):
        if not self.session:
            self.session = aiohttp.ClientSession(raise_for_status=True)
            self.session_pool[self.scenari.get('url')]=self.session
            return await self._request(**self.scenari)
        else:
            # print('nous sommes là !!')
            return await self._request(**self.scenari)






if __name__ == '__main__':

    with closing(asyncio.get_event_loop()) as loop:
        con = Connect({'action':'post_request','url':GUICHET_ADRESSE, 'data':CODES })
        loop.run_until_complete(con.do_scenari())
