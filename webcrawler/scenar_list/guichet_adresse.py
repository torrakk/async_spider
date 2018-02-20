GUICHET_ADRESSE = 'https://guichet-adresse.ign.fr/map'
##
##Exemple avec l'url guichet adresse, si nous voulons suivre les lien , il faut les rajouter en links puis nous pouvons parser dans
##ces derniers avec l'option parse
linkss = {

        'parse': [
                  {'selection': [{'find_all': {'type': 'a', }},
                                 ],
                   'results': {'text': 'attribut3'},
                   'mapping_fields': [],
                   'with_parents': []
                   }
                  ],
        'links': None,
        'scenari': False,
        'session': None,
        'inject': {},
        'follow':False
    }


dicto = [{'action': 'get',
   'url': GUICHET_ADRESSE,
   'data': '',
   'parse':[{'selection': [{'find_all': {'type': 'input', 'name':'_csrf_token'}}
                           ],
             'results': {'name':'attribut1','type':'attribut2', 'value':'attribut3'},
             'mapping_fields': [],
             },
            {'selection': [{'find_all': {'type': 'a',}}
                           ],
             'results': {'text':'attribut1','target':'attribut2', 'href':'attribut3'},
             'mapping_fields': [],
             },
            ],
   'links': linkss,
   'scenari': [],
   'session':None,}]

