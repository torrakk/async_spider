import re
data_servitude_haute_loire = 'https://www.data.gouv.fr/fr/search/?q=servitude+haute-loire'
# Téléchargement des données relatives aux servitudes d'utilité publiques de la ddt de la haute loire

linkss = {
        'parse': [{'selection': [{'find_all': {'type': 'a', 'href': re.compile(u'format=SHP&projection=WGS84')}},
                                     ],
                       'results': {'href': 'href', 'title': 'attribut2', 'text': 'attribut3'},
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
   'parse':[{'selection': [{'find_all': {'type': 'a', 'href':re.compile('-servitude-')}}
                                                       ],
                                         'results': {'href':'href','title':'attribut2', },
                                         'mapping_fields': [],
                                         },
            ],
   'links': linkss,
   'scenari': [],
   'session':None,}]