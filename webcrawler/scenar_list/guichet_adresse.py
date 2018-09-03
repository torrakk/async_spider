GUICHET_ADRESSE = 'https://guichet-adresse.ign.fr/login'
##
##Exemple avec l'url guichet adresse, si nous voulons suivre les lien , il faut les rajouter en links puis nous pouvons parser dans
##ces derniers avec l'option parse
# linkss = {
#
#         'parse': [
#                   {'selection': [{'find_all': {'type': 'a', 'href':re.compile('')}},
#                                  ],
#                    'results': {'text': 'attribut3', 'href':'href'},
#                    'mapping_fields': [],
#                    'with_parents': []
#                    }
#                   ],
#         'links': None,
#         'scenari': False,
#         'session': None,
#         'inject': {},
#         'follow':False
#     }


dicto = [{'action': 'get',
   'url': GUICHET_ADRESSE,
   'data': '',
    'parse':[#{'selection': [{'find_all': {'name': 'input', "name":"_csrftoken"}}
   #                         ],
   #           'results': {'name':'name','type':'typo', 'value':'csrf_token'},
   #           'mapping_fields': [],
   #           },
            {'selection': [{'find_all': {'name': 'a',}}
                           ],
             'results': {'text':'attribut1','target':'attribut2', 'href':'href'},
             'mapping_fields': [],
             },
             {'selection': [{'find_all': {'name': 'div', 'class':"form-group"}}, {'find_all': {'name': 'input', 'class':'form-control'}}
                           ],
             'results': {'id':'id unique', 'name':'name','type':'type de saisie', 'class':'classe'},
             'mapping_fields': [],
             },
            ],
   'links': [], #linkss,#linkss, #linkss,
   'scenari': [],
   'session':None,}]

