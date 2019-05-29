import re
from collections import OrderedDict
bet_click_url = 'https://www.google.fr/search?hl=fr&tbm=isch&source=hp&biw=1920&bih=925&ei=TePrXI6uIdLIwQKNtb64BA&q=test&oq=test&gs_l=img.3..0l10.2062.2587..2785...0.0..0.192.439.3j1......0....1..gws-wiz-img.....0.d-_p9xm5r3A'
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
              ## faire un infinite scroll
              ##https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

                                      ('find_elements_by_css_selector', 'img.rg_ic.rg_i'),
                                      ('nested',
                                              [
                                               ('click', None),
                                                'nested',[
                                               ('find_elements_by_css_selector', 'div.immersive-container'),
                                               ('send_keys', 'Keys.ESCAPE')
                                                ]
                                                ## TODO il faut pouvoir appliquer la méthode suivante https://gist.github.com/lrhache/7686903 et non pas le back
                                               ]
                                       )
                                     # ('click', None),
                                     # ('find_elements_by_css_selector', 'label.spriteFlags'),
                                     # ('click', None),

                                     #{'find_all': {'name': 'span', 'class': "SpriteFlags"}}
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