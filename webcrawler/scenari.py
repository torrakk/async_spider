import asyncio
from contextlib import closing

from webcrawler.parser import Parse
from webcrawler.connecteur import Connect

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

    def __init__(self, **kwargs):
        self.future = asyncio.Future()
        self.kwargs = kwargs
        actions = ['loop', 'action', 'url', 'data', 'parse', 'scenari', 'session']
        Counter.tasks += 1
        # print(Counter.tasks)
        assert list(self.kwargs.keys()) == actions, \
            "Votre scenari est malformé, " \
            "il manque des informations " \
            "{} doit être {}".format(list(self.kwargs.keys()), actions)

        for attr, value in kwargs.items():
            if attr in actions:
                setattr(self, attr, value)

    def validate(self):
        '''
        Cette fonction permet de verifier un scenari
        :return: 
        '''

    async def connect(self):
        '''
        Cette fonction permet se connecter à une page avec une methode get ou post
        Nous preparons les arguments pour qu'ils ne concernent que l'action à engagé
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
        self.kwargs['scenari'].update({'session': self.session})
        scenar = scenari(loop=self.loop, **self.kwargs['scenari'])
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
        self.future.add_done_callback((self.callback_scenari if self.kwargs['scenari']!=[] else self.print_fut))
        # try:
        self.session, page = await self.connect()
        return self.future.set_result(Parse(page).list_parse(self.parse)) if self.parse \
        else self.future.set_result(page)
        # except (TypeError) as e:
        #     print("nous stoppons il y a un problème de connexion {}".format(e))
        #     self.loop.stop()

    def __repr__(self):
        return(str(self.__dict__))


# if __name__=="__main__":
#     with closing(asyncio.get_event_loop()) as loop:
#         con = Connect({'action': 'post_request', 'url': GUICHET_ADRESSE, 'data': CODES})
#         loop.run_until_complete(con.do_scenari())