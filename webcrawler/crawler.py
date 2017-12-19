import asyncio
import time
import re

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

    linkss = {
                'parse': [{'selection': {'type': 'a', 'href': re.compile(u'format=SHP&projection=WGS84')},
                           'resultat': {'attrs': ['href', 'title', 'text']}}],
                'links':None,
                'scenari':False,
                'session': None,
                'inject': {},
                'follow': True
             }

    links = {
             'parse': [{'selection': {'type': 'a', 'href': re.compile('zC21Q6t0KL9ly')},
                        'resultat': {'attrs': ['href','title', 'text']}}],
             'links': None,
             'scenari': False,
             'session': None,
             'inject': {},
             'follow': False
            }


    robot = Crawler(scenario=[{'action': 'get',
                               'url': GUICHET_ADRESSE,
                               'data': CODES,
                               'parse':[{'selection': [{'find_all': {'type': 'div'}}, {'find_all': {'type': 'a', 'href': True}}
                                                       ],
                                         'results': {'href':'attribut1','title':'attribut2', 'text':'attribut3'},
                                         'mapping_fields': [],
                                         'with_parents': []
                                         }],
                               'links': links,
                               'scenari': [],
                               'session':None,}
                              ]
                            , loop=loop )
    # print(loop)
    parse_guichet_adresse = {'selection': {'type': 'input', 'name': '_csrf_token'},
     'resultat': {'attrs': ['value', 'text'], }}, {'selection': {'type': 'input', 'name': '_submit'},
                                                   'resultat': {'attrs': ['value', 'text']}}
    robot.do_scenari()
