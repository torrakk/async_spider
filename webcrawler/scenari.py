import asyncio
import time
from logging2 import Logger
import re

from webcrawler.parser import Parse
from webcrawler.connecteur import Connect
from webcrawler.utils import validateUrl, joinUrl
from webcrawler.log import scenari_log
from webcrawler.mapper import mapp



class Counter():
    tasks = 0


class scenari(object):
    '''
    Un scenari est un objet cappable de se connecter et de s'appeler de manière recursive en passant 
    les attributs d'une page web scrapper à une autre
    
    le scenari se sert des objets futures pour
    1) Se connecter à la page 
    2) Parser ce qu'il y a à parser
    3) Ajouter un scenari enfant avec le resultat de 1 et 2
    
    Plusieurs cas possibles sont identfiés :
    
    
    
    
    
                                         /---> cas 1 : Nous parsons et injectons les données---> si un scenari est défini
                                        /              nous revenons au debut du schema, voir télécharger des données si
                                        /              si c'est un zip
                          parsage      /
    1) visite d'une page ---------------------> cas 2 : Nous suivons les liens pour parser ( et/ou pas ) injecter les
                                       \               données, voir télécharger des données.
                                        \              
                                         \
    
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
    ## variable de classe permettant de stocker touts les url visitées
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
        self.page = "Page vide"
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
    def __dataSearch(self, data, datasearch):
        '''
        Fait une recherche des données resultats pour les injecter dans les datas
        envoyées lors du post
        :param data: 
        :param datasearch: 
        :return: 
        '''
        #1 va chercher la données à reprendre
        reg = re.compile('^init(.*)')
        donnee = [reg.match(datakeys) for datakeys in data.keys()]

    async def connect(self):
        '''
        Cette fonction permet se connecter à une page avec une methode get ou post
        Nous preparons les arguments pour qu'ils ne concernent que l'action à engager
        :return: 
        '''
        scenari_log.info('future connexion : ' + str(self.kwargs['url']) )
        co = Connect(self, **{ key: value for key, value in self.kwargs.items() if key in ('action', 'url', 'data', 'session')})
        return await co.request()

    def callback_scenari(self, future):
        '''
        Methode permettant de se servir de la session ouverte pour continuer à travailler 
        avec les données reçues et les cookies
        Pour cela nous injectons l'objet en tant que future dans la boucle evenementielle
        :return: 
        '''
        Counter.tasks -= 1
        scenari_log.debug("Nous en sommes à la tâche : {}".format(Counter.tasks))
        scenari_log.debug('Nous sommes dans le callback : ' + str(future.result()))
        #print("Nous sommes dans le callback: " , future.result())
        # log.info(future.result())
        ##Nous suivons les liens en produisant en scenari sans aboutir à un parsage

        if self.kwargs['links'] and not None in future.result():
            scenari_log.info('Nous traitons les liens {}'.format(self.kwargs['links']))
            self.followLinks(self.kwargs, future.result())

        if self.scenari and type(self.scenari) is not bool:
            scenari_log.info('Nous traitons un scenario {}'.format(self.scenari))
            self.kwargs['scenari'].update({'session': self.session})
            scenari_log.debug('Nous sommes dans le callback : ' + str(future.result()))
            scenar = scenari(loop=self.loop, **self.kwargs['scenari'])
            asyncio.gather(scenar.run())
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

    def modeleUpdateProducer(self, link, kwargs):
        '''
        Méthode permettant de valider les links et construire un modele de scenario
        à partir des information de l'objet
        :param link: 
        :return: True Or False(si nous pouvons visiter l'url), modele (et le modele mis en forme)
        '''
        href = link.get('href', None)
        #print('HREF :', href, " , " ,link)
        #scenari_log.debug("Nous tentons de vérifier l'existence d'un lien {} {}".format(link, kwargs))
        url = validateUrl(href, joinUrl(self.url, href)).__next__()
        #print('url ', url)


        ##Nous vérifions l'url, si elle existe, si elle est bien formée puis nous produisons un scenari

        if not url in self.url_visited:
            #print(self.url_visited)
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
            return True, modele
        else:
            scenari_log.info("Nous ne visiterons pas l'url {} car elle a déjà été visitée".format(url))
            return

    def followLinks(self, kwargs, result):

        scenari_log.debug("resultats dans le follow links : "+str(result))
        assert isinstance(result, list)
        ## Produit un scenari par resultat
        for links in result:
            # try:
            assert isinstance(links, list)
            for link in links:
                if self.modeleUpdateProducer(link, kwargs):
                    validite, modele = self.modeleUpdateProducer(link, kwargs)
                    scenar = scenari(loop=self.loop, **modele)
                    asyncio.gather(scenar.run())
                else:
                    scenari_log.debug("on passe à côté \n" + str(kwargs))
            ### Si nous avons des erreurs de Type ou de clé sur certains champs
            ### alors nous ne pouvons pas produire de link
            # except (TypeError, KeyError) as e:
            #     if 'href' in str(e):
            #         scenari_log.error("\n\nErreur Les links sont : ",e ," " , links , "\n\n")



    def print_fut(self, future):
        Counter.tasks -= 1
        #print('Counter.tasks: ', Counter.tasks)
        scenari_log.info('Counter Tasks : '+ str(Counter.tasks))
        scenari_log.info("Nous sommes dans le print futures : " + str(future.result()))
        self.__decoLoop()


    async def run(self):
        '''
        Méthode permettant de crawler une page web et d'ajouter un callback en cascade.
        :return: 
        '''
        self.future.add_done_callback((self.callback_scenari if self.kwargs['scenari'] or self.kwargs['links'] else self.print_fut))

        try:
            self.session, self.page = await self.connect()
        except (TypeError) as e:
            #print("Nous sommes dans l'erreur")
            scenari_log.error('Erreur {} \n {}'.format(e,self.kwargs))

        # print(Parse(self.page).getList(self.parse))
        return self.future.set_result(Parse(self.page).list_parse(self.parse)) if self.parse \
        else self.future.set_result(self.page)

    def __repr__(self):
        return(str(self.__dict__))


# if __name__=="__main__":
#     with closing(asyncio.get_event_loop()) as loop:
#         con = Connect({'action': 'post_request', 'url': GUICHET_ADRESSE, 'data': CODES})
#         loop.run_until_complete(con.do_scenari())