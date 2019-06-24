import re
from collections import OrderedDict
bet_click_url = 'https://infinite-scroll.com/demo/full-page/'
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

                                      ('find_elements_by_css_selector', 'article.article'),
                                      ('find_elements_by_css_selector', 'h2'),
                                      ('find_elements_by_css_selector', 'a'),

                                      # ('nested',
                                      #         [
                                      #          ('click', None),
                                      #          ('back', None), ## TODO il faut pouvoir appliquer la méthode suivante https://gist.github.com/lrhache/7686903 et non pas le back
                                      #          ]
                                      #  )
                                     # ('click', None),
                                     # ('find_elements_by_css_selector', 'label.spriteFlags'),
                                     # ('click', None),

                                     #{'find_all': {'name': 'span', 'class': "SpriteFlags"}}
                                 ],
                    'results': {'href':'lien'},
                    'mapping_fields': [],
                   }
                  ],
          'links': None,
          'scenari': [],
          'session':None,
          'javascript': True
          }
         ]