parents = {'parse': [{'selection': [{'find_all': {'type': 'div'}}, {'find_all': {'type': 'a', 'href': True}}
                           ],
           'resultat': {'attrs': {'href':'attribut', 'title':'attribut2', 'text':'attribut3'}},
                     }]
           }

## Voici une présentation du modèle d'objet à parser
## Description des sections
     # 'parse' : Permet de parser de manière récursive plusieurs éléments en s'appuyant sur Beautiful Soup,
     #           nous pouvons nous servir de n'importe qu'elle méthode beautiful soup
     # 'results': Permet d'avoir les résultats demandés sous forme de dictionnaire et d'avoir un attribut de référence
     #             pour chaque résultat. Ces attributs seront utilisés pour l'injection de données
     #  #'with_parents': Permet d'aller chercher des balises parentes pour les intégrer aux résultats --<
     #    Nous l'enlevons car nous pouvons le faire en ajoutant une balise a parser
     #  'mapping_fields': Permet de mettre en relation des résultats avec un modèle Django

enfants = {'parse': [{'selection': [{'find_all': {'type': 'div'}}, {'find_all': {'type': 'a', 'href': True}}
                           ],
           'results': {'href':'attribut', 'title':'attribut2', 'text':'attribut3'},
           'mapping_fields': 'model'
                      }]
           }
