import re
data_servitude_haute_loire = 'https://www.data.gouv.fr/fr/search/?q=servitude+haute-loire'
# Téléchargement des données relatives aux servitudes d'utilité publiques de la ddt de la haute loire
#'text': re.compile(u'export SHP/WGS-84')
linkss = {
        'parse': [{'selection': [{'find_all': {'name': 'article',
                                               'class_' : 'card',
                                               # 'string' : re.compile('.*WGS-84.*')
                                               }},
                                 {'find_all': {'name': 'h4', 'string' : re.compile('.*WGS-84.*')}},
                                 {'find_parent': 'article'},
                                 {'find': 'footer'},
                                 {'find': {'name': 'a', 'string' : re.compile('Télécharger')}}
                                 #{'find': 'footer'}
                                     ],
                       'results': {'class': 'classe', 'href': 'href', 'text': 'text'},
                       'duplicates': True,
                       },
                  ],
        'links': [],
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