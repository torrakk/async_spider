import asyncio
import time
from logging2 import Logger


from webcrawler.parser import Parse
from webcrawler.connecteur import Connect
from webcrawler.utils import validateUrl, joinUrl
from webcrawler.log import scenari_log



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
    
    Plusieurs cas possibles sont identfiés :
    
    
    
    
    
                                         /---> cas 1 : Nous parsons et injecons les données---> si un scenari est défini
                                        /              nous revenons au debut du schema, voir télécharger des données si
                                        /              si c'est un zip
                          parsage      /
   1) visite d'une page ---------------------> cas 2 : Nous suivons les liens pour parser ( et/ou pas ) injecter les
                                       \               données, voir télécharger des données.
                                        \              
                                         \
                                          \---> cas 3 : 
    '''
    modele_scenari = {
                      'action':None,
                      'url':None,
                      'data':None,
                      'parse':None,
                      'links':None,
                      'scenari':None,
                      'session':None,
                    }

    url_visited = set()

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
        
        Plusieurs cas sont possible :
        1) nous voulons visiter une page et la parser --> injection des données
        2) nous voulons visiter une page, la parser, suivre les liens +/- injection des données
        3) nous voulons visiter une page, la parser, suivre les liens --> télécharger des données
        
        '''
        self.future = asyncio.Future()
        self.kwargs = kwargs

        actions = ['loop', 'action', 'url', 'data', 'parse', 'links', 'scenari', 'session']
        Counter.tasks += 1
        # print(Counter.tasks)
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
        # print("Nous en sommes à la tâche :", Counter.tasks)
        scenari_log.debug('Nous sommes dans le callback : ' + str(future.result()))
        #print("Nous sommes dans le callback: " , future.result())
        # log.info(future.result())
        ##Nous suivons les liens en produisant en scenari sans aboutir à un parsage
        if self.kwargs['links'] :
            scenari_log.debug('Nous traitons les liens {}'.format(self.kwargs['links']))
            self.followLinks(self.kwargs, future.result())

        if self.scenari and type(self.scenari) is not bool:
            scenari_log.debug('Nous traitons un scenario {}'.format(self.scenari))
            self.kwargs['scenari'].update({'session': self.session})
            scenar = scenari(loop=self.loop, **self.kwargs['scenari'])
            asyncio.ensure_future(scenar.run())
        # print("url visitée 1 fois: ", len(self.url_visited),"\n", self.url_visited, "\n")
        self.__decoLoop()

    def __decoLoop(self):
        if Counter.tasks == 0:
            scenari_log.info('Nous fermons la loop')
            # Nous fermons toutes les sessions ouvertes
            for url, session in Connect.session_pool.items():
                #print('nous détruisons la session')
                session.close()
            self.loop.stop()

    def followLinks(self, kwargs, result):

        # print(result)
        ## Produit un scenari par resultat
        for links in result:
            try:
                for link in links:
                    href = link.get('href', None)
                    url = href if validateUrl(href) else joinUrl(self.url, href)
                    ##Nous vérifions l'url, si elle existe, si elle est bien formée puis nous produisons un scenari
                    if not href in self.url_visited and href:
                        modele = self.modele_scenari.copy()
                        modele.update({
                        'action': 'get',
                        'url': url,
                        'data': None,
                        ## Nous allons chercher le parse du link donc l'url nous est remontée
                        'parse': kwargs.get('links', [])['parse'],
                        'links': kwargs.get('links', []),
                        'scenari': True,
                        'session': None})
                        scenari_log.info("Nous allons visiter l'url via follow, {}".format(modele['url']))
                        scenar = scenari(loop=self.loop, **modele)
                        asyncio.ensure_future(scenar.run())
            ### Si nous avons des erreurs de Type ou de clé sur certains champs
            ### alors nous ne pouvons pas produire de link
            except (TypeError, KeyError) as e:
                if 'href' in str(e):
                    scenari_log.debug("\n\nErreur Les links sont : ",e ," " , links , "\n\n")

    # def produceLinks(self, links, page):
    #     '''
    #     Cette méthode permet de parser la page à partir du type de lien à parser
    #     de recupérer les urls et de produire des objets scenari à partir de cela
    #     :return:
    #     '''
    #     print("les Links ",links['parse'])
    #     links_parse = Parse(page).list_parse(links['parse'])
    #
    #     for list_balise in links_parse:
    #         for link in list_balise:
    #             if self.links['scenari'] and validateUrl(joinUrl(self.url, link['href']))  \
    #                     and not joinUrl(self.url, link['href']) in self.url_visited:
    #
    #                 modele = self.modele_scenari.copy()
    #                 self.url_visited.add(joinUrl(self.url, link['href']))
    #                 parse = None
    #                 if  self.links['links'] :
    #                     if self.links['links']['links']:
    #                         parse = self.kwargs['links']['links']['parse']
    #
    #                 modele.update({
    #                      'action': 'get',
    #                      'url': link['href'] if validateUrl(link['href']) else joinUrl(self.url, link['href']),
    #                      'data': None,
    #                      'parse': parse,
    #                      'links': self.links['links'],
    #                      'scenari': True,
    #                      'session': None})
    #                 print("Nous allons visiter l'url via produce links, ", modele['url'])
    #                 scenar = scenari(loop=self.loop, **modele)
    #                 asyncio.ensure_future(scenar.run())
    #             else:
    #                 print("url déja visitée 1 fois: ", len(self.url_visited),'\nurl déjà visitée : ',joinUrl(self.url, link['href']), "\n")

    def print_fut(self, future):
        Counter.tasks -= 1
        # print(Counter.tasks)
        print("Nous sommes dans le print futures : ", future.result())
        self.__decoLoop()


    async def run(self):
        '''
        Méthode permettant de crawler une page web et d'ajouter un callback en cascade.
        :return: 
        '''
        self.future.add_done_callback((self.callback_scenari if self.kwargs['scenari'] or self.kwargs['links'] else self.print_fut))
        self.session, self.page = await self.connect()
        # print(Parse(self.page).getList(self.parse))
        return self.future.set_result(Parse(self.page).list_parse(self.parse)) if self.parse \
        else self.future.set_result(self.page)

    def __repr__(self):
        return(str(self.__dict__))


# if __name__=="__main__":
#     with closing(asyncio.get_event_loop()) as loop:
#         con = Connect({'action': 'post_request', 'url': GUICHET_ADRESSE, 'data': CODES})
#         loop.run_until_complete(con.do_scenari())