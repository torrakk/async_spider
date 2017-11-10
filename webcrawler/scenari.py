import asyncio
import time



from webcrawler.parser import Parse
from webcrawler.connecteur import Connect
from webcrawler.utils import validateUrl, joinUrl
# from webcrawler.crawler import crawlTime



class Counter():
    tasks = 0


class scenari():
    '''
    Un scenari est un objet cappable de se connecter et de s'appeler de manière recursive en passant 
    les attributs d'une page web scrapper à une autre
    
    le scenari se sert des objets futures pour
    1) Se connecter à la page 
    2) Parser ce qu'il y a à parser
    3) Ajouter un scenari enfant avec le resultat de 1 et 2
    
    '''
    modele_scenari = {
                      'action':None,
                      'url':None,
                      'data':None,
                      'parse':None,
                      'links':None,
                      'scenari':None,
                      'session':None}

    def __init__(self, **kwargs):
        '''
        Lors de l'initialisation nous demandons les arguments suivants
        
        :param kwargs:
        loop : boucle initialisée pour pouvoir arrêter cette dernière lorsque nous avons fini de crawler
        action : type d'action souhaitée (post, get, put, delete)
        url : url à visiter
        data : les données à envoyer si post
        parse:: les balises à parser dans la page --> voir la doc du parser pour voir les synthaxes
        links : Les liens à suivre (produit des objets scenari en cascade pour parser d'autres pages)
        scenari : suite de l'algorithme autre page à visiter
        session : Session ouverte (objet clientSession) si le site est le même
        
        '''
        self.future = asyncio.Future()
        self.kwargs = kwargs

        actions = ['loop', 'action', 'url', 'data', 'parse', 'links', 'scenari', 'session']
        Counter.tasks += 1
        # print(self.count)
        assert list(self.kwargs.keys()) == actions, \
            "Votre scenari est malformé, " \
            "il manque des informations " \
            "{} doit être {}".format(list(self.kwargs.keys()), actions)

        for attr, value in kwargs.items():
            if attr in actions:
                setattr(self, attr, value)

    def __validate(self):
        '''
        En cours de dev. Cette fonction permettra de verifier un scenari.
        :return: 
        '''

    async def connect(self):
        '''
        Cette fonction permet se connecter à une page avec une methode get ou post
        Nous preparons les arguments pour qu'ils ne concernent que l'action à engager
        :return: 
        '''
        co = Connect(**{ key: value for key, value in self.kwargs.items() if key in ('action', 'url', 'data', 'session')})
        return await co.request()

    def callback_scenari(self, future):
        '''
        Methode permettant de se servir de la session ouverte pour continuer à travailler 
        avec les données reçues et les cookies
        Pour cela nous injectons l'objet en tant que future dans la boucle evenementielle
        :return: 
        '''
        Counter.tasks -= 1
        print(future.result())
        # print(self.kwargs)
        if  self.kwargs['links']:
            self.produceLinks(self.kwargs['links'], self.page)

        if self.scenari and type(self.scenari) is not bool:
            self.kwargs['scenari'].update({'session': self.session})
            scenar = scenari(loop=self.loop, **self.kwargs['scenari'])
            asyncio.ensure_future(scenar.run())

    def produceLinks(self, links, page):
        '''
        Cette méthode permet de parser la page à partir du type de lien à parser
        de recupérer les urls et de produire des objets scenari à partir de cela
        :return: 
        '''

        links_parse = Parse(page).list_parse(links['parse'])
        for list_balise in links_parse:
            for link in list_balise:
                if self.kwargs['links']['scenari']:

                    modele = self.modele_scenari.copy()
                    modele.update({
                         'action': 'get',
                         'url': link['href'] if validateUrl(link['href']) else joinUrl(self.url, link['href']),
                         'data': None,
                         'parse': self.kwargs['links']['futur_parse'],
                         'links': self.links['links'],
                         'scenari': True,
                         'session': None})
                    scenar = scenari(loop=self.loop, **modele)
                    asyncio.ensure_future(scenar.run())

    def print_fut(self, future):
        Counter.tasks -= 1
        print(future.result())
        if Counter.tasks == 0:
            # Nous fermons toutes les sessions ouvertes
            for url, session in Connect.session_pool.items():
                session.close()
            self.loop.stop()

    async def run(self):
        self.future.add_done_callback((self.callback_scenari if self.kwargs['scenari'] or self.kwargs['links'] else self.print_fut))
        # self.future.add_done_callback((self.callback_scenari if self.kwargs['links'] != [] else self.print_fut))#or self.kwargs['links']!=[]
        # try:
        self.session, self.page = await self.connect()
        return self.future.set_result(Parse(self.page).list_parse(self.parse)) if self.parse \
        else self.future.set_result(self.page)
        # except (TypeError) as e:
        #     print("nous stoppons il y a un problème de connexion {}".format(e))
        #     self.loop.stop()

    def __repr__(self):
        return(str(self.__dict__))


# if __name__=="__main__":
#     with closing(asyncio.get_event_loop()) as loop:
#         con = Connect({'action': 'post_request', 'url': GUICHET_ADRESSE, 'data': CODES})
#         loop.run_until_complete(con.do_scenari())