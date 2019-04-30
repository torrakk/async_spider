####
# Le parser permet d'aller chercher les éléments qui nous interessent dans la page web

####
from bs4 import BeautifulSoup
import bs4
from itertools import chain

from webcrawler.utils import reorgPaquetGenerator
from webcrawler.log import parse_log
from webcrawler.mapper import mapp
from webcrawler.utils import xpath

class Parse():

    def __init__(self, page):
        '''
        Le parser permet de parser une page web en fonction d'une liste de balise et de retourner une selection 
        nous pouvons soit parser une liste de balise, soit une seule.
        voir les méthodes : parse et list_parse
        :param page: 
        '''



        self.page = page
        self.soup = BeautifulSoup(self.page, 'html.parser')



    def list_parse(self, list_baliz ):
        '''
        Permet de parser une liste de balise
        
        :param list: parse une liste de kwargs
        :return: 
        List_resultat
        '''
        return [self.parse(**baliz) for baliz in list_baliz] if list_baliz else self.page

    def __mapp(self, orig, results):
        '''
        Méthode permettant de mettre en relation les résultats avec les attributs finaux demandés 
        dans le dictionnaire de données
        :param orig: 
        :param results: 
        :return: 
        '''
        assert isinstance(orig, dict) == True
        assert isinstance(results, dict) == True
        try:
            return {v: results[k] for k, v in orig.items()}
        except(KeyError):
            print("le mapping est incorrect \n-orig : {0}\n-reuslts : {1}".format(orig, results))


    def __getBFmethod(self, resu, cle):
        '''
        Méthode permettant d'accéder aux méthodes de beautifulSoup
        :param resu: 
        :param cle: 
        :return: 
        '''
        if hasattr(resu, cle):
            return getattr(resu, cle)
        return

    def resultSetIter(self, resultSet):
        for result in resultSet:
            yield result

    @xpath
    def rechercheBF(self, motif, element):
        '''
        Recherche BF est un generateur permettant de lancer 
        de manière recursive des coroutines de recherche
        
        :param motif: tuple typeRecherche, valeursDeRecherche
        :param element: bs4.BeautifulSoup or bs4.element.ResultSet
        :param objetRetour: Variable a laquelle assigner une liste de resultat permettant de 
        continuer la recherche
        :return: resultat de recherche
        '''

        typeRecherche, valeursDeRecherche = list(motif.items())[0]
        parse_log.info("Nous sommes dans la fonction {0} valeursDeRecherche:{1} ".format(typeRecherche, valeursDeRecherche))
        ## TODO: Il faut faire du debug ici afin de pouvoir faire un click sur un objet sans fournir d'argument Voir le dernier if (ça merde encore après modifications)
        try:
            if isinstance(element, bs4.element.ResultSet) or isinstance(element, list):
                obj = [ self.rechercheBF(motif, result) for result in element ]
                parse_log.debug('BeautifulSoup !' + type(element) +  'typeRecherche : ' + typeRecherche) #+ " element bs :" + element)
                objetRetour = obj if not isinstance(obj[0], list) else list(chain.from_iterable(obj))#list(chain.from_iterable(obj))
            elif isinstance(element, bs4.BeautifulSoup) or isinstance(element, bs4.element.Tag):
                #print('NOUS SOMMES DANS UN ELEMENT BeautifulSoup !', type(element), element)
                parse_log.debug('BeautifulSoup !' + str(type(element)) + 'typeRecherche : ' + typeRecherche) #+ " element bs :" + str(element))
                #print("ok")
                if isinstance(valeursDeRecherche, dict):
                    print("Nous sommes ici 1")
                    objetRetour = self.__getBFmethod(element, typeRecherche)(**valeursDeRecherche)
                    #print(objetRetour)
                if isinstance(valeursDeRecherche, str):
                    print("Nous sommes là 2")
                    objetRetour = self.__getBFmethod(element, typeRecherche)(valeursDeRecherche)
                if not valeursDeRecherche:
                     print("Nous sommes là 3")
                     objetRetour = self.__getBFmethod(element, typeRecherche)()
            #print("\nType d'objet retour : ", type(objetRetour), "\nType-valeurs de recherche : ",typeRecherche , " : ", valeursDeRecherche, "\nObjet retour : ", objetRetour)
            return objetRetour
        except(Exception) as e:
            print(e)
            raise
        #print(" !!! \n\n Nous sommes dans un cas special ", type(element))

    def parse(self, **kwargs):

        '''
        
        Permet de faire de recherche de balise et de les retourner sous forme de dictionnaire
        :param objet: recherche un objet contenu dans une balise
               kwargs : {'selection':{'type':None, 'classe':None, 'value':None, 'regex':None}, 
                         'resultat':{'text':'', 'attr':['liste des attributs']}}}
               Le selection permet de fair eune selection des balises et le résultat permet 
               de faire remonter les données attendues
        :return:
    
        '''


        try:
            assert type(self.page)==str, "La page doit être de type string"
        except AssertionError:
            return


        selection, resultat, with_parents = kwargs['selection'].copy(), kwargs['results'].copy(),\
                                  kwargs.get('with_parents', None)

        page_bf = self.soup
        result = []
        parse_log.debug("selection :\n" + str(selection))
        #parse_log.debug("page affichée :\n" + self.page)
        #     ##faire un iterateur qui renvoi une exception en cas de fin d'iteration
        self.result_partiel = None
        for selectionMotif in selection:
            ## Si il existe un resultat partiel alors celui-ci est affecté à l'élément sinon
            ## nous prennons la page bf4
            element = self.result_partiel if self.result_partiel else page_bf
            self.result_partiel = self.rechercheBF(selectionMotif, element)


        #Permet de renvoyer des résultats non dupliqués si des balises similaires ressortent
        if kwargs.get('duplicates', None):
            #TODO tester si cela passe au niveau du duplicates
            for item in self.result_partiel:
                if not item in result:
                    result.append(item)
        else:
            result = self.result_partiel
        # for i in result:
        #     print(type(i), i, len(i))
            # for g in i:
            #     print(type(g), g)
        ## TODO : tester avec betclick pour que l'on retourne toutes les valeurs des matchs et developper le mapping fields pour que nous puissions injecter directement avec django
        ##
        if result:
            parse_log.debug("resultat du parseur" + str(result) +str([i.__dict__ for i in result])+ " type : "+ str(type(result)))
            #parse_log.debug("{}".format([[(item.__dict__, item.get(cle)) if cle != 'text' else item.getText().strip() for cle in resultat.keys()] for item in result ]))
            return [self.__mapp(resultat, {cle: item.get(cle) if cle != 'text' else item.getText().strip()
                                                       for cle in resultat.keys()}) for item in result ]
        else:
            parse_log.debug("Le parseur ne trouve pas de résultat")
            return

    def getList(self, list_baliz):
        '''
        Permet d'obtenir une liste des balises demandées
        :param list_baliz: 
        :return: 
        '''
        recherche = self.list_parse(list_baliz)
        resultante = min([len([item.values() for item in  item_recherche if item.values()]) for item_recherche in recherche])
        return list(zip(*[[j  for j in reorgPaquetGenerator(i, resultante) if j ] for i in recherche]))


if __name__=='__main__':
    # heure_debut_rencontre = {'selection':{'type':'span', 'class':'KambiBC-event-item__start-time--time'},
    #                  'resultat':{'attrs':['class', 'text']}}
    # sport = {'selection':{'type':'span', 'class':'KambiBC - modularized - event - path__fragment'},
    #                  'resultat':{'attrs':['class', 'text']}
    #          }
    # competition = {'selection':{'type':'span', 'class':'KambiBC-modularized-event-path__fragment'},
    #                  'resultat':{'attrs':['class', 'text']}
    #          }
    # participants = {'selection': {'type': 'div', 'class':'KambiBC-event-participants__name'},
    #                  'resultat': {'text': '','attrs': ['text']}}
    # paris = {'selection': {'type': 'span', 'class': 'KambiBC-mod-outcome__odds'},
    #                'resultat': {'attrs': ['class', 'text']}}
    # nb_offre_de_paris = {'selection': {'type': 'span', 'class': 'KambiBC-event-item__bet-offer-count'},
    #          'resultat': {'attrs': ['class', 'text']}}
    html ='''
    <html>
       <body>
           <div class="test 1">
                
                    <h1>Titre esssai</h1>
                    <h2>Sous  titre</h2>
                
           </div>
           <div class='balise1'>
                <span>
                    <h1>Titre esssai 1</h1>
                    <h2>Sous  titre 1</h2>
                </span>
                <span>
                    <h1>Titre esssai 2</h1>
                    <p><h3 class="type1">La ferme de pigeons</h3><h3 class="type1">Le projet des teubés</h3></p>
                    <h2>Sous  titre 2</h2>
                </span>
           </div>
           <div class="test3">
                <span>
                    <h1>Titre esssai 3</h1>
                    <p><h3 class="type1">La ferme de pigeons 2</h3><h3 class="type1">Le projet des teubés 3</h3></p>
                    <h2>Sous  titre 3</h2>
                </span>
           </div>
           <div></div>
       </body>
    </html>
    '''
    # soup = BeautifulSoup(html, 'html.parser')
    # print(soup.html.body.div.span.__getattribute__('parent'))
    a = Parse(html).parse(duplicates=True, **{'selection': [{'find_all': {'name': 'div',}},
                                           {'find_all': {'name': 'span'}},
                                           {'find_all': {'name': 'h2',}},
                                           {'find_parent': 'div'},
                                           {'find_all': {'name': 'h3'}},
                                                       ],
                                         'results': {'class':'classe', 'name':'name', 'xpath':'xpath', 'text': 'texte'},
                                         'mapping_fields': [],
                                         }
                        )
    print(a)
    # for i in a:
    #     print(i)