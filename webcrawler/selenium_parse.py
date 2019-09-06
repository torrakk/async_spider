from itertools import chain
from abc import ABC, abstractmethod

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, \
    ElementNotSelectableException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import traceback
import time
import re

from webcrawler.utils import reorgPaquetGenerator
from webcrawler.log import sele_log
from webcrawler.mapper import mapp
from webcrawler.utils import xpath
from webcrawler.settings import PAUSE

def action(recherches):
    '''
    Générateurs sur les actions
    :param recherches:
    :return:
    '''
    rank = 0
    length = len(recherches)
    for item in recherches:
        rank += 1
        yield item

def lastSearchAction(recherches):
    '''
    Fait remonté la dernière action de recherche, avec son type de retour
    :param recherches:
    :return:
    '''

def getItemType(item):
    """
    Cette fonction permet de retourner le type de retour de la fonction
    :param item:
    :return: list, single or None
    """
    try:
        doc = item.__doc__.strip().replace("\n", "")
    except(AttributeError):
        doc = ''
    DOCSTRING_LIST_WEBELEMENT = re.compile('^.*:Returns:.*- (list of WebElement).*$')
    DOCSTRING_WEBELEMENT = re.compile('^.*:Returns:.*- (WebElement).*$')
    if DOCSTRING_LIST_WEBELEMENT.match(doc):
        return "list"
    elif DOCSTRING_WEBELEMENT.match(doc):
        return "single"
    elif item in ('click', 'drag_and_drop', 'back'):
        return
    return

def rechercheDsElement(element, methode):
    pass


class rechercheSelenium():

    '''
    Permet de faire une recherche en chaine d'éléments selenium
    la recherche selenium produit des objets chaineDeRecherche
    '''

    def __init__(self, page, recherche):
        pass




class chaineDAction():
    '''
    La chaîne d'action permet d'avoir un objet contenant tous les éléments d'une chaîne de recherche
    Le chaine permet de faire toute la recherche en une fois. CAD nous allons tout de suite a l'élément le plus profond.
    Une chaîne est produite par élément recherché. Chaque élément est de type webElement au nous allons ajouter des méthodes
    et attributs.
    La chaîne d'actions permet d'executer des actions dans une page de remonter les éléments et de les comparer
    Nous fournissons aux différents éléments les méthodes avec lesquelles ils doivent rechercher.
    '''

    ##Variables contenant tous les éléménts, plusieurs chaineDeRecherchent peuvent être inclues.
    resultats = set([])

    def __init__(self, recherches, page):
        '''
        :param recherches: chaines de recherches
        :param page: Webdriver instancié
        '''

        # crée un generateur qui permet de prendre les actions les unes après les autres
        self.action = action(recherches)
        self.page = page
        self.chaine = set([])

    def finAction(self):
        """
        Acte la fin de recherche pour une chaîne de recherche
        :return:
        """
        if all((element.retour for element in self.chaine)):
            return True
        return False

    def chaineAction(self):
        '''
        Permet d'excuter une suite d'actions. Ces dernières vont être menées jusqu'au bout, c'est à dire que nous executerons
        le suite d'action sur un élément avec de passer à un autre.
        :return:
        '''
        while not self.finAction():
            webelems = webElements(next(self.action), self.page)
            self.chaine = webelems.run(self)
            
            # TODO Mettre en place ici la recherche des webelements
            # TODO il faut faire une fonction recursive qui rappel chaineAction afin que nous allions toujours



from types import MethodType
# https://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc
class webElements():
    '''
    Serie d'éléments remontés d'une recherche, sur une fenêtre (windowAction)
    L'objet webelement pilote l'objet windowAction qui se deplace sur la page.
    1) Nous faisons l'action dans la page --> methode run
        1-a) Si l'action conduit à une recherche d'autres éléments alors nous produisons
             une chaine d'action --> chaineAction
        1-b) Si l'action ne mêne à rien ou ne renvoie rien alors nous faisons un --> Return True
    Les actions sont soit enregistrées dans un resultat dans webElements soit dans un resultat de chainAction si ce sont les derniers
    '''

    PAUSE = 4

    def __init__(self, recherche, page ):
        self.page = page
        self.url = self.page.getCurrentUrl()
        self.action = recherche
        self.window = windowAction(self.page)

    def __getSeleniumMethod(self, resu, cle):
        '''
        Méthode permettant d'accéder aux méthodes de de selenium
        :param resu:
        :param cle:
        :return:
        '''
        print(set(map(type, resu)), " : " , cle)
        try:
            if hasattr(resu, cle):
                #print('l\'element {} possede la methode {}'.format(resu, cle))
                return getattr(resu, cle)
            else:
                return getattr(self.page, cle)
        except(Exception) as e:
            print("La methode selenium ne semble pas exister {}".format(cle))
            raise

    def seleniumActionBase(self, item, action, args=None):

        try:
            methodeSelenium = self.__getSeleniumMethod(item, action)
        except(Exception) as e:
            print(e, traceback.format_exc())
            print("L'objet {} n'a pas de méthode {}".format(item, action))
            raise
        return methodeSelenium(args) if args else methodeSelenium()

    def run(self, item, action, args=None):

        '''
        Methode permettant de rechercher de faire une recherche dans la page
        :param item: element selenium
        :param action: Methode selenium a appliquer
        :param args: Arguments accompagnant la methode selenium
        :return:
        '''

        onContinue = True
        inter = set([])

        #La boucle ici permet de rechercher des éléments à l'intérieur de la fenêtre courante

        while onContinue:
            try:
                trouve = self.seleniumActionBase(item, action, args)
                typoItem = getItemType(item)
                if typoItem == 'liste' and trouve:
                    for item in trouve:
                         inter.update(item)
                elif typoItem == 'single' and trouve:
                    inter = trouve
            except(Exception) as e:
                print(e, traceback.format_exc())
                raise
            ## Si nous sommes au dernier rang de recherche alors nous
            ## continuons la recherche

            ## TODO finir la problématique ici, soit il faut continuer le scroll, si nous sommes au dernier rang de recherche
            ## TODO ajouter l'éléments père à la chaîne d'action pour que l'élément enfant puisse dire au père d'avancer
            ## TODO modifier le calcul de rang car un generateur ne va pas, il faudrait le mettre dans les webelements et chaineDAction
            ## TODO Il faut faire un dialogue entre webelements et chaineDAction
            if action.rank == action.length:
                onContinue = self.window.scroll()
            ## Sinon nous ne scrollons pas et continuons la recherche en profondeur
            else:
                chaineDAction()


        # print("List inter :", [i.tag_name for i in inter])
        return list(inter) if inter else None

class windowAction():
    '''
    Objet fenetre permettant de déplacer la fenêtre dans la page cet objet fenetre est controlé par l'objet
    WebElements
    '''
    PAUSE = PAUSE

    def __init__(self, session):
        self.page = session
        self.page.execute_script("window.scrollTo(0, 0)")
        self.lastHeight = 0
        self.newHeight = 0
        ## Fixe le endpage à false
        self._endpage = False
        ## permet au script de continuer de scroller
        self.oncontinue = True
        print("initialisation de windowAction")

    def refresh(self):
        '''
        Permet un rafraîchissement du DOM de la page
        :return:
        '''
        self.page.refresh()
        self.startOfDoc()
        self.moove(self.newHeight)

    def scroll(self):

        while self.oncontinue:
            try:
                ## Deplace la fenetre de visibilite sur la page
                print("Debut du moove")
                self.moove()
                # self.page.implicitly_wait(self.PAUSE)

                time.sleep(self.PAUSE)
                self.newHeight = self.getHeight()
                sele_log.debug("Nouvelle hauteur mesurée {}".format(self.newHeight))
                if self.newHeight == self.lastHeight:
                    self.startOfDoc()
                    self._endpage = True
                    ## Nous renvoyons le False pour signifier l'arrêt de la recherche à la méthode infiniteScrollLocalize
                    ## de la classe webelements
                    return False, self.newHeight
                yield True
            except(Exception) as e:
                sele_log.debug(traceback.format_exc())
                print(e, traceback.format_exc())
                raise
            self.lastHeight = self.newHeight


    @property
    def endpage(self):
        return self._endpage

    def getHeight(self):
        '''Permet d'obtenir le hauteur actuelle de la fenêtre'''
        try:
            return self.page.execute_script("return document.documentElement.scrollHeight;")
        except(Exception) as e:
            sele_log.debug(traceback.format_exc())
            print(e, traceback.format_exc())
            raise

    def moove(self, height=None, direction='Down'):
        '''
        Permet de bouger la fenêtre de la taille du navigateur de haut en bas
        :return:
        '''
        if not height:
            height = self.getHeight()
        height = height if direction is 'Down' else -1*height
        sele_log.debug("Nous sommes dans le moove {}".format(height))
        try:
            self.page.execute_script("window.scrollBy(0, {});".format(height))
        except(Exception) as e:
            sele_log.debug(traceback.format_exc())
            print(e, traceback.format_exc())
            raise

    def startOfDoc(self):
        self.page.execute_script("window.scrollTo(0, 0)")




class webElement():
    '''
    L'objet webElement est une classe contenant des méthodes qui seront ajoutés aux objet webelement de selenium.
    Pour ce faire nous avons choisi le pattern de composition. La composition permettra d'executer, la méthode correspondante.
    '''

    def __init__(self, webElement):
        self.chainepere = None
        self.chainefils = None
        self.retour = False

    def method(self, methode):
        """
        Permet de jouer la methode proposee à ce niveau
        :return: retour de la methode excutée
        """
        self.retour = True
        self._method = self.method
        return self._method()

    @property
    def __hash__(self):
        """
        Le hash est défini en fonction du texte contenu dans l'objet
        TODO la methode de hash doit être faite sur l'objet webelement prit en argument
        :return:
        """
        return hash(self.getText)

    def __eq__(self, other):
        '''
        Comparateur de webelement
        :param value:
        :return:
        '''
        if self.__hash__ == hash(other):
            return True
        return False