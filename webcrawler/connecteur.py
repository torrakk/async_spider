import re
import aiohttp
import asyncio
from contextlib import closing
import socket
import random

from webcrawler.settings import *


class Connect(object):
    # Variable permettant de partager les sessions en fonction des urls visitées et les fermer proprepement /
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
        self.test_url = re.compile('^http(s)?:\/\/.*\..*$')
        self.action = self.scenari.pop('action')
        self.session = self.scenari.pop('session', None)
        if self.scenari['url'] in self.session_pool.keys():
            self.session = self.session_pool[self.scenari['url']]


    def test_url(self, url):
        if not self.test_url.match(url):
            raise('Votre url est malformée')

    async def _request(self, **kwargs):
        '''
        
        :param url: page demandée
        :return: 
        '''
        # print('nous sommes en get')
        try:
                async with self.session.__getattribute__(self.action)(**kwargs) as response:
                    return (self.session, await response.text())
        except (aiohttp.client_exceptions.ClientResponseError, aiohttp.client_exceptions.ClientConnectorError, socket.gaierror) as e:
            print('Nous avons un problèmes de connexion au site --> {}'.format(e))

    async def request(self):
        if not self.session:
            self.session = aiohttp.ClientSession(raise_for_status=True)
            # print('nous sommes ici !')
            self.session_pool[self.scenari.get('url')]=self.session
            # print(self.session_pool)
            return await self._request(**self.scenari)
        else:
            # print('nous sommes là !!')
            return await self._request(**self.scenari)






if __name__ == '__main__':

    with closing(asyncio.get_event_loop()) as loop:
        con = Connect({'action':'post_request','url':GUICHET_ADRESSE, 'data':CODES })
        loop.run_until_complete(con.do_scenari())
