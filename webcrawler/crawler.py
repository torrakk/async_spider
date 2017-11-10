import asyncio
import time

from webcrawler.scenari import scenari, Counter
from webcrawler.settings import *

class crawlTime():
    def time(self):
        duree = time.time() - Crawler.heure_debut
        return ("durée webcrawl: {:08.2f} s".format(duree))


class Crawler():
    heure_debut = time.time()
    def __init__(self, scenario, loop):

        self.loop = loop
        self.scenario = scenario

    def do_scenari(self):

        [asyncio.ensure_future(scenari(loop=self.loop, **kwargs).run()) for kwargs in self.scenario]

        try:
            self.loop.run_forever()
        finally:
            print(crawlTime().time())
            self.loop.close()

                # self.loop.run_until_complete(asyncio.gather(*tasks))


if __name__=="__main__":
    loop = asyncio.get_event_loop()

    links = {
             'parse': [{'selection': {'type': 'a'},
                        'resultat': {'attrs': ['href','title', 'text']}}],
             'futur_parse':[{'selection': {'type': 'a'},
                        'resultat': {'attrs': ['href','title', 'text']}}],
             'links':[],
             'scenari':True,
             'session':None,
             'inject': {}, 'follow': True}
    a = {'action': 'get', 'url': GUICHET_ADRESSE, 'data': CODES,
     'parse': [{'selection': {'type': 'input', 'name': '_csrf_token'},
                'resultat': {'text': '', 'attrs': ['value', ], }}]  , 'links':links,'scenari':[], 'session':None}
    # print(loop)
    robot = Crawler(scenario=[{'action': 'get', 'url': GUICHET_ADRESSE, 'data': CODES, 'parse':[{'selection':{'type':'input', 'name':'_csrf_token'},
                                                                                                            'resultat':{'attrs':['value', 'text'], }}, {'selection':{'type':'input', 'name':'_submit'},
                                                                                                            'resultat':{'attrs':['value', 'text'] }}]
                                                                                                  , 'links': links,'scenari': a, 'session':None} #for i in range(0,500)

                            ]
                            , loop=loop )
    # print(loop)
    robot.do_scenari()
