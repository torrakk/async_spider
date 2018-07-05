import re
data_servitude_haute_loire = 'https://www.data.gouv.fr/fr/search/?q=servitude+haute-loire'
# Téléchargement des données relatives aux servitudes d'utilité publiques de la ddt de la haute loire
#'text': re.compile(u'export SHP/WGS-84')
linkss = {
        'parse': [{'selection': [{'find_all': {'name': 'article',
                                               'class_' : 'card',
                                               # 'text' : re.compile('.*WGS-84.*')
                                               }}, {'find_all': {'name': 'h4',}},
                                     ],
                       'results': {'class': 'classe', 'href': 'href', 'text': 'text'},
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


dicto = [{'action': 'get',
   'url': data_servitude_haute_loire,
   'data': '',
   'parse':[{'selection': [{'find_all': {'name': 'a', 'href':re.compile('-servitude-')}}
                                                       ],
                                         'results': {'href':'href','title':'attribut2', },
                                         'mapping_fields': [],
                                         },
            ],
   'links': linkss,
   'scenari': [],
   'session':None,}]