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
    for item in recherches:
        yield item

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

    def __init__(self, recherches, webdriver):
        self.recherches = action(recherches)
        self.webdriver = webdriver
        self.chaine = set([])

    def finRecherche(self):
        """
        Acte la fin de recherche pour une chaîne de recherche
        :return:
        """
        if all((element.retour for element in self.chaine)):
            return True
        return False

    def recherche(self):
        while not self.finRecherche():
            pass


from types import MethodType
# https://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc

# class composition(ABC):

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
        self.page.navigate().refresh()
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
                    return False, self.newHeight
                return True, self.newHeight
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
        # try:
        return self.page.execute_script("return document.documentElement.scrollHeight;")
        # except(Exception) as e:
        #     sele_log.debug(traceback.format_exc())
        #     print(e, traceback.format_exc())
        #     raise

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

class webElements():
    '''
    Serie d'éléments remontés d'une recherche, sur une fenêtre (windowAction)
    L'objet webelement pilote l'objet windowAction qui se deplace sur la page.
    '''

    PAUSE = 4
    DOCSTRING_LIST_WEBELEMENT = re.compile('^.*:Returns:.*- (list of WebElement).*$')
    DOCSTRING_WEBELEMENT = re.compile('^.*:Returns:.*- (WebElement).*$')

    def __init__(self, recherche, page ):
        self.page = page
        self.action = recherche
        self.window = windowAction(self.page)

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


        #La boucle ici permet de rechercher des éléments à l'intérieur de la fenêtre courante

        while onContinue:
            try:
                trouve = self.seleniumRechercheBase(item, action, args)
                # print(trouve, self.DOCSTRING_LIST_WEBELEMENT.match(itemDoc), self.DOCSTRING_WEBELEMENT.match(itemDoc))
                if (self.DOCSTRING_LIST_WEBELEMENT.match(itemDoc) or itemDoc is '') and trouve:
                    for item in trouve:
                        inter.update(item)
                elif self.DOCSTRING_WEBELEMENT.match(itemDoc) and trouve:
                    return trouve
                elif item in ('click', 'drag_and_drop', 'back'):
                    self.window.refresh()
                    return None
            except(Exception) as e:
                print(e, traceback.format_exc())
                raise
            onContinue, newHeight = self.window.scroll()

        # print("List inter :", [i.tag_name for i in inter])
        return list(inter) if inter else None


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