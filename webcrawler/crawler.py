import asyncio
import re
import time


from webcrawler.scenari import scenari
# from webcrawler.scenar_list.guichet_adresse import dicto
from webcrawler.scenar_list.open_data_servitudes_hautes_loire import dicto

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
             'parse':None,
             'links': [],
             'scenari': False,
             'session': None,
             'inject': {},
             'follow': False
            }
    ## Le parse permet de suivre les liens cherchés dans la recherche parente.
    ## En l'occurence ici dans le robot
    ## L'option follow permet soit
    # linkss = {
    #
    #     'parse': [{'selection': [{'find_all': {'type': 'a', 'href': re.compile(u'format=SHP&projection=WGS84')}},
    #                              ],
    #                'results': {'href': 'attribut1', 'title': 'attribut2', 'text': 'attribut3'},
    #                'mapping_fields': [],
    #                'with_parents':  []
    #                },
    #               {'selection': [{'find_all': {'type': 'h2', }},
    #                              ],
    #                'results': {'text': 'attribut3'},
    #                'mapping_fields': [],
    #                'with_parents': []
    #                }
    #               ],
    #     'links': None,
    #     'scenari': False,
    #     'session': None,
    #     'inject': {},
    #     'follow': True
    # }
    # robot = Crawler(scenario=[{'action': 'get',
    #                            'url': GUICHET_ADRESSE,
    #                            'data': CODES,
    #                            'parse':[{'selection': [{'find_all': {'type': 'a', 'href':re.compile('servitude')}}
    #                                                    ],
    #                                      'results': {'href':'attribut1','title':'attribut2', 'text':'attribut3'},
    #                                      'mapping_fields': [],
    #                                      },
    #                                     {'selection': [{'find_all': {'type': 'meta'}}
    #                                                    ],
    #                                      'results': {'name': 'attribut1', 'property': 'attribut2', 'content': 'attribut3'},
    #                                      'mapping_fields': [],
    #                                      }
    #                                     ],
    #                            'links': linkss,
    #                            'scenari': [],
    #                            'session':None,}
    #                           ]
    #                         , loop=loop )
    # # print(loop)
    # parse_guichet_adresse = {'selection': {'type': 'input', 'name': '_csrf_token'},
    #  'resultat': {'attrs': ['value', 'text'], }}, {'selection': {'type': 'input', 'name': '_submit'},
    #                                             'resultat': {'attrs': ['value', 'text']}}
    robot = Crawler(scenario=dicto, loop=loop)
    robot.do_scenari()
