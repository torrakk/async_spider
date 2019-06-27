####
# Le parser permet d'aller chercher les éléments qui nous interessent dans la page web

####
from bs4 import BeautifulSoup
import bs4
from itertools import chain
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, \
    ElementNotSelectableException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import traceback
import time
import re

from webcrawler.utils import reorgPaquetGenerator
from webcrawler.log import parse_log
from webcrawler.mapper import mapp
from webcrawler.utils import xpath

class Parse():

    webdriver = WebDriver
    PAUSE = 4
    DOCSTRING_LIST_WEBELEMENT = re.compile('^.*:Returns:.*- (list of WebElement).*$')
    DOCSTRING_WEBELEMENT = re.compile('^.*:Returns:.*- (WebElement).*$')

    def __init__(self, session):
        '''
        Le parser permet de parser une page web en fonction d'une liste de balise et de retourner une selection 
        nous pouvons soit parser une liste de balise, soit une seule.
        voir les méthodes : parse et list_parse
        :param session: l'objet session
        '''

        parse_log.debug("Nous parsons la page {}".format(type(session)))
        if isinstance(session, self.webdriver):
            parse_log.debug("Recherche de type selenium")
            self.typeRecherche = self.rechercheSelenium
            self.page = session
        elif isinstance(session, str):
            parse_log.debug("Recherche de type BeautifulSoup")
            self.typeRecherche = self.rechercheBF
            self.page = BeautifulSoup(self.page, 'html.parser')

    def list_parse(self, list_baliz ):
        '''
        Permet de parser une liste de balise en appelant la methode parse
        
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
            return [(v, results[k]) for k, v in orig.items()]
        except(KeyError):
            print("le mapping est incorrect \n-orig : {0}\n-results : {1}".format(orig, results))


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

    def __getSeleniumMethod(self, resu, cle):
        '''
        Méthode permettant d'accéder aux méthodes de beautifulSoup
        :param resu:
        :param cle:
        :return:
        '''
        if hasattr(resu, cle):
            #print('l\'element {} possede la methode {}'.format(resu, cle))
            return getattr(resu, cle)
        else:
            return getattr(self.page, cle)
        return

    def resultSetIter(self, resultSet):
        for result in resultSet:
            yield result
    #
    # def rechercheSelenium(self, motif, element):
    #     continue
    # def rechercheSelenium(self, motif, element):

    @xpath
    def rechercheBF(self, motif, element):
        '''
        Recherche BF est un generateur permettant de lancer 
        de manière recursive des coroutines de recherche beautiful soup
        
        :param motif: tuple typeRecherche, valeursDeRecherche
        :param element: bs4.BeautifulSoup or bs4.element.ResultSet
        :param objetRetour: Variable a laquelle assigner une liste de resultat permettant de 
        continuer la recherche
        :return: resultat de recherche
        '''

        typeRecherche, valeursDeRecherche = list(motif.items())[0]
        parse_log.debug("Nous sommes dans la fonction {0} valeursDeRecherche:{1}, element: {2} ".format(typeRecherche, valeursDeRecherche, type(element)))

        try:
            if isinstance(element, bs4.element.ResultSet) or isinstance(element, list):
                parse_log.debug('BeautifulSoup ! 1 ' + type(element) + 'typeRecherche : ' + typeRecherche)
                obj = [ self.rechercheBF(motif, result) for result in element ]
                objetRetour = obj if not isinstance(obj[0], list) else list(chain.from_iterable(obj))#list(chain.from_iterable(obj))
            elif isinstance(element, bs4.BeautifulSoup) or isinstance(element, bs4.element.Tag):
                parse_log.debug('BeautifulSoup ! 2 ' + str(type(element)) + 'typeRecherche : ' + typeRecherche ) #"" element bs :" + str(element))
                if isinstance(valeursDeRecherche, dict):
                    objetRetour = self.__getBFmethod(element, typeRecherche)(**valeursDeRecherche)
                if isinstance(valeursDeRecherche, str):
                    objetRetour = self.__getBFmethod(element, typeRecherche)(valeursDeRecherche)
            return objetRetour
        except(Exception) as e:
            print("Nous sommes dans une exception du parseur {}".format(e))
            raise
        #print(" !!! \n\n Nous sommes dans un cas special ", type(element))





    # def infiniteScrollSearch(self, item, action, args=None):
    #     '''
    #     La methode infinite scroll search permet de faire des recherches d'éléments
    #     en faisant un scroll infini dans toutes la page
    #     :param item:
    #     :param action:
    #     :param args:
    #     :return:
    #     '''
    #     pause = 4 ## 4 secondes de pause pour le chargement
    #     onContinue = True
    #     inter = set([])
    #     ## Nous remontons en haut de la page
    #     self.page.execute_script("window.scrollTo(0, 0)")
    #
    #     #print('nous cherchons dans les éléments {}'.format(type(item), item.text if type(item) != type(self.page) else ''))
    #     while onContinue:
    #         try:
    #             trouve = self.seleniumRechercheBase(item, action, args)
    #             if trouve:
    #                 inter.update(set(trouve))
    #             lastHeight = self.page.execute_script("return document.body.scrollHeight")
    #             self.page.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             time.sleep(self.PAUSE)
    #             newHeight = self.page.execute_script("return document.body.scrollHeight")
    #             if newHeight == lastHeight:
    #                 onContinue = False
    #             lastHeight = newHeight
    #
    #         except(Exception) as e:
    #             print(e, traceback.format_exc())
    #             raise
    #
    #     return list(inter)

    # def rechercheNestedSelenium(self, selection, resultats):
    #     '''
    #     Permet d'effecteur une recherche sur les éléments inclus dans des recherches
    #     :param selection:
    #     :param resultats:
    #     :return:
    #     '''
    #
    #     #select = (i for i in selection)
    #     resultat = resultats
    #     parse_log.debug("resultats nested: " + str(resultat))
    #     # try:
    #     for item in resultat:
    #         print("Nous sommes à l'item nested {}".format(item))
    #         select = (i for i in selection)
    #         resultat_inter = ''
    #         while select:
    #             print("PETITE PAUSE \n\n")
    #             time.sleep(self.PAUSE)
    #             try:
    #                 action, args = next(select)
    #                 print("Nous faisons l'action {} {} ".format(action, args))
    #                 if action == "nested":
    #                     self.rechercheNestedSelenium(args, resultat if resultat else None)
    #                 else:
    #                     trouve = self.infiniteScrollLocalize(item, action, args)
    #                 if trouve:
    #                     resultat_inter += trouve
    #             except(TypeError) as e:
    #                 print(e, traceback.format_exc())
    #                 raise
    #             except(StaleElementReferenceException):
    #                 inter = self.infiniteScrollLocalize(item, action, args)
    #                 if not inter:
    #                     print("\n ## Nous n'avons pas trouvé l'élément \n ")
    #             except(StopIteration):
    #                 print('Nous avons chopé l\'exception de sortie')
    #                 break
    #
    #     ## Retour à la page principale
    #     self.page.switch_to_window(self.pagePrincipale)
    #
    #     return resultat_inter

    def scroll(self, lastHeight):
        '''
        Permet le scroll
        :return:
        '''
        try:
            self.page.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            #self.page.implicitly_wait(self.PAUSE)
            time.sleep(self.PAUSE)
            newHeight = self.page.execute_script("return document.documentElement.scrollHeight")
            if newHeight == lastHeight:
                self.page.execute_script("window.scrollTo(0, 0)")
                return False, newHeight
            return True, newHeight
        except(Exception) as e:
            print(e, traceback.format_exc())
            raise

    def seleniumRechercheBase(self, item, action, args=None):

        try:
            methodeSelenium = self.__getSeleniumMethod(item, action)
        except(Exception) as e:
            print(e, traceback.format_exc())
            print("L'objet {} n'a pas de méthode {}".format(item, action))
            raise
        return methodeSelenium(args) if args else methodeSelenium()


    def infiniteScrollLocalize(self, item, action, args=None):
        '''
        Methode permettant de rechercher un élément dans la page en scrollant
        :param item: element selenium
        :param action: Methode selenium a appliquer
        :param args: Arguments accompagnant la methode selenium
        :return:
        '''

        onContinue = True
        inter = set([])
        try:
            itemDoc = item.__doc__.replace('\n', '')
        except(AttributeError):
            itemDoc = item.__doc__
        finally:
            if not itemDoc:
                itemDoc = ''

        ## Nous remontons en haut de la page
        self.page.execute_script("window.scrollTo(0, 0)")
        #print("Remontée en haut de page")
        #print('nous cherchons dans l\'élément {} l\'élément {}'.format(type(item), item.text if type(item)!=type(self.page) else '' ))
        lastHeight = self.page.execute_script("return document.documentElement.scrollHeight")
        while onContinue:
            try:
                trouve = [self.__mapp(self.resultat, {cle: item.get_attribute(cle) or getattr(item, cle, '') if cle != 'text' else item.getText().strip() if hasattr(item, 'getText') else item.text
                                                       for cle in self.resultat.keys()}) for item in self.seleniumRechercheBase(item, action, args) ]

                #print(trouve, self.DOCSTRING_LIST_WEBELEMENT.match(itemDoc), self.DOCSTRING_WEBELEMENT.match(itemDoc))
                if (self.DOCSTRING_LIST_WEBELEMENT.match(itemDoc) or itemDoc is '') and trouve:
                    for item in trouve:
                        inter.update(item)
                elif self.DOCSTRING_WEBELEMENT.match(itemDoc) and trouve:
                    return trouve
                elif item in ('click', 'drag_and_drop'):
                    return None
            except(Exception) as e:
                print(e, traceback.format_exc())
                raise

            onContinue, newHeight = self.scroll(lastHeight)
            lastHeight = newHeight

        #print("List inter :", [i.tag_name for i in inter])
        return list(inter) if inter else None

    def rechercheSelenium(self, selection, resultats=None):
        """
        Nous chainons les methodes selenium les unes aux autres
        Plusieurs recherches différentes peuvent être réalisées
        -1 recherche classiques de plusieurs éléments
        -2 Recherches classique puis à partir des cette dernière -- > recherche d'éléments imbriqués -
        cad que nous allons aller vers un groupe d'éléments puis revenir au principal

        :param methodes: Dictionnaires des méthodes
        :return:
        """
        parse_log.debug('Nous chainons les méthodes selenium')
        # methodes_chaines = "self.page."+ ".".join(["{}(**{})".format(func, args) if isinstance(args, dict) else \
        #     "{}({})".format(func, "'{}'".format(str(args)) if args else '')  for item in selection for func, args in item.items()])
        # parse_log.debug(methodes_chaines)


        ## Page principale de référence
        self.pagePrincipale = self.page.current_window_handle

        # nous faisons un generateur
        select = (i for i in selection)

        if not resultats:
            action_prem, args = next(select)
            resultat = self.infiniteScrollLocalize(self.page, action_prem, args)
        else:
            resultat = resultats
        # try:

        while select:
            resultat_inter = ''
            try:
                action, args = next(select)
                parse_log.debug("action args : {} {}".format(action, args))

                if isinstance(resultat, list) or isinstance(resultat, set):
                    resultat_inter = set([])
                    #parse_log.debug('Nous avons plusieurs resultats :\n{} {}'.format(args, str([i.text for i in resultat])))
                    for result_uniq in resultat:
                        try:
                            resultat_inter.update(self.infiniteScrollLocalize(result_uniq, action, args))
                        except(TypeError):
                            resultat_inter.update([])
                            ## si la liste est vide, nous ne pouvons pas itérer dessus
                elif isinstance(resultat, self.page._web_element_cls):
                    parse_log.debug(
                        'Nous avons un resultat unique :\n{} {}'.format(args, resultat.text))
                    resultat_inter = self.infiniteScrollLocalize(self.page, action, args)
                resultat = resultat_inter if resultat_inter else resultat
                parse_log.debug(
                    'Resultat :\n{}'.format(resultat))
            except(StopIteration):
                parse_log.debug(
                    '''Signal d\'arrêt d\'iteration' :{}\n{}'''.format(args, resultat))
                resultat = resultat_inter if resultat_inter else resultat
                break
            except(Exception) as e:
                print(e, traceback.format_exc())
                raise

        return resultat
        # except(Exception) as e:
        #     print(e, traceback.format_exc())
        #     raise


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


        # try:
        #     assert type(self.page)==str, "La page doit être de type string"
        # except AssertionError:
        #     return


        selection, self.resultat, with_parents = kwargs['selection'].copy(), kwargs['results'].copy(),\
                                  kwargs.get('with_parents', None)

        #page_bf = self.soup
        result = []
        parse_log.debug("selection :\n" + str(selection))
        #parse_log.debug("page affichée :\n" + self.page)
        #     ##faire un iterateur qui renvoi une exception en cas de fin d'iteration
        self.result_partiel = None
        if isinstance(self.page, self.webdriver):
            self.result_partiel = self.rechercheSelenium(selection)
        elif isinstance(self.page, str):
            for selectionMotif in selection:
                ## Si il existe un resultat partiel alors celui-ci est affecté à l'élément sinon
                ## nous prennons la page bf4
                element = self.result_partiel if self.result_partiel else self.page
                #print("Objet en retour dans boucle des motifs {}, result partiel : {}".format(selectionMotif, type(self.result_partiel)))
                self.result_partiel = self.typeRecherche(selectionMotif, element)


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
            # print(result)
            #parse_log.debug("resultat du parseur" + str(result) +str([i.__dict__ for i in result])+ " type : "+ str(type(result)))
            #parse_log.debug("{}".format([[(item.__dict__, item.get(cle)) if cle != 'text' else item.getText().strip() for cle in resultat.keys()] for item in result ]))
            resultat = [self.__mapp(resultat, {cle: item.get_attribute("href") or getattr(item, cle, '') if cle != 'text' else item.getText().strip() if hasattr(item, 'getText') else item.text
                                                       for cle in resultat.keys()}) for item in result ]
            print(resultat)
            return resultat
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