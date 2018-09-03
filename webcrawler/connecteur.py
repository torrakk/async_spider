import re
import os
import aiohttp
import asyncio
from contextlib import closing
import socket
from abc import *
from selenium import webdriver
import random
# from logging2 import Logger


from webcrawler.settings import *
from webcrawler.exception import *
from webcrawler.utils import validateUrl
from webcrawler.log import connect_log

class Connect(object):
    # Variable permettant de partager les sessions en fonction des urls visitées et les fermer proprement /
    # une fois que ces dernières ont été visitées
    session_pool = {}

    def __init__(self, scenar_obj,**scenar):
        '''
        L'objet connect permet de se connecter au guichet adresse et d'interrragir avec ce dernier
        :param adresse: adresse à laquelle se connecter (chaine de caractère)
        :param credentials: login et mdp contenues dans un dictionnaire
        '''
        #self.session = session
        self.scenar = scenar
        self.scenar_obj = scenar_obj
        self.action, self.session = (self.scenar.pop(keys) for keys in ('action', 'session'))
        # si une session existe quelque part nous la prennons

        if not self.session:
            self.session = self.session_pool[self.scenar['url']] if self.scenar['url'] in self.session_pool.keys() \
                else self.scenar.pop('session', None) or None

        self.download_path = STATIC_PATH
        self.nomfichier = re.compile(r'\"(?P<nomfichier>.*)\"')

    def testUrl(self, url):
        if not validateUrl(url):
            print(url)
            #print('Votre url est malformée')
            raise testUrlError('Votre url est malformée')

    def _requestJS(self, **kwargs):
        self.testUrl(kwargs['url'])
        connect_log.info('url visitée : {}'.format(kwargs['url']))
        try:
            driver = webdriver.Firefox()
            #Attente implicite de 1 a 3 secondes
            driver.implicity_wait(random.randint(1, 3)),
            self.scenar_obj.url_visited.add(kwargs.get('url'))
            return driver.__getattribute__(self.action)(**kwargs)
        except(Exception) as e:
            print("Nous n'arrivons pas à afficher la page\nerreur:{}".format(e))


    async def _request(self, **kwargs):
        '''
        
        :param url: page demandée
        :return: 
        '''

        self.testUrl(kwargs['url'])
        connect_log.info('url visitée : {}'.format(kwargs['url']))
        try:
            print(self.session.__dict__)
            async with self.session.__getattribute__(self.action)(**kwargs) as response: #timeout=TIMEOUT,
                connect_log.debug(str("url : "+ kwargs.get('url') + "\nResponse status : "+str(response.status)+"\nHeaders : " + str(response.headers)))
                assert response.status == 200
                self.scenar_obj.url_visited.add(kwargs.get('url'))
                if response.headers.get('Content-Type') == 'application/zip':
                    #print("Nous sommmes lalalalalalalala !!!!!!!!")
                    connect_log.debug(response.headers.get('Content-Disposition'))
                    nom_fichier = (self.nomfichier.search(( response.headers.get('Content-Disposition'))).group('nomfichier'))
                    with open(os.path.join(self.download_path, nom_fichier), 'wb') as fichier:
                        while True:
                            #print("Nous sommmes icic !!!!!!!!")
                            chunk = await response.content.read()
                            #print('Téléchargement de ', nom_fichier, ' ', len(chunk),' kbits')
                            if not chunk:
                                break
                            fichier.write(chunk)
                            connect_log.info("Téléchargement de {}".format(nom_fichier))
                            connect_log.info("Le fichier pèse : {0} {1}".format(os.path.getsize(os.path.join(self.download_path, nom_fichier))/1024, " ko"))
                    return (self.session,  None)
                return (self.session, await response.text())
        except (aiohttp.client_exceptions.ClientError, aiohttp.client_exceptions.ClientResponseError, aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ClientOSError, socket.gaierror) as e:
            connect_log.debug('Nous avons un problèmes de connexion au site {}--> {}'.format(kwargs['url'], e,))
            #print('Nous avons un problèmes de connexion au site --> {}'.format(e))

    async def request(self):
        if not self.session:
            self.session = aiohttp.ClientSession(raise_for_status=True)
            #self.session._default_headers.update({"User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
            print(self.session._default_headers)
            self.session_pool[self.scenar.get('url')]=self.session
            return await self._request(**self.scenar)
        else:
            # print('nous sommes là !!')
            return await self._request(**self.scenar)






if __name__ == '__main__':

    with closing(asyncio.get_event_loop()) as loop:
        con = Connect(**{'action':'get','url':'http://www.loire-semene.fr/', 'data':CODES , 'session': None })
        requete = loop.run_until_complete(con.request())
        print(requete)
        requete[0].close()