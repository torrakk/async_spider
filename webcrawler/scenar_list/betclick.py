import re
from collections import OrderedDict
bet_click_url = 'https://www.betclic.fr/calendrier-0'
# Téléchargement des données relatives aux servitudes d'utilité publiques de la ddt de la haute loire

linkss = {
        'parse': [{'selection': [{'find_all': {'type': 'input', 'name':'_csrf_token'}}
                           ],
             'results': {'name':'name','type':'typo', 'value':'csrf_token'},
             'mapping_fields': [],
             },

            {'selection': [{'find_all': {'type': 'div', 'class':'market_matchName'},
                                  'find_all': {'type': 'a'}
                                  },
                                     ],
                       'results': {'href': 'attribut1', 'text': 'match_name'},
                       'mapping_fields': [],
                       'with_parents': []
                       },
                  ],
        'links': None,
        'scenari': False,
        'session': None,
        'inject': {},
        'follow':True
    }


dicto = [
         {'action': 'get',
          'url': bet_click_url,
          'data': '',
          'parse':[{'selection': [
                                   OrderedDict([
                                       ('find_all', {'name': 'span', 'class' : "calendar_sportList_sportName"}),
                                       ('click', {}),
                                       ('find_all', {'name': 'span', 'class': "SpriteFlags"})
                                   ])
                                 ],
                    'results': {'text':'contenu', 'xpath':'xpath'},
                    'mapping_fields': [],
                   }
                  ],
          'links': None,
          'scenari': [],
          'session':None,
          'javascript': True
          }
         ]