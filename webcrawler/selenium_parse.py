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
from webcrawler.log import parse_log
from webcrawler.mapper import mapp
from webcrawler.utils import xpath


def rechercheDsElement(element, methode):



class rechercheSelenium():

    '''
    Permet de faire une recherche en chaine d'éléments selenium
    la recherche selenium produit des objets chaineDeRecherche
    '''

    def __init__(self, page, recherche):
        pass

class chaineDeRecherche():
    '''
    La chaîne de recherche permet d'avoir un objet contenant tous les éléments d'une chaîne de recherche
    Le chaine permet de faire toute la recherche en une fois. CAD nous allons tout de suite a l'élément le plus profond.
    Une chaîne est produite par élément recherché. Chaque élément est de type webElement au nous allons ajouter des méthodes
    et attributs.
    La chaîne de recherche permet de rechercher dans une page les éléments et de les comparer
    Nous fournissons aux différents éléments les méthodes avec lesquelles ils doivent rechercher.
    '''

    ##Variables contenant tous les éléménts, plusieurs chaineDeRecherchent peuvent être inclues.

    def __init__(self, recherches, webdriver):
        self.recherches
        self.webdriver
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



from types import MethodType
# https://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc

# class composition(ABC):


class webElement():
    '''
    L'objet webElement est une classe contenant des méthodes qui seront ajoutés aux objet webelement de selenium.
    Pour ce faire nous avons choisi le pattern de composition. La composition permettra d'executer, la méthode correspondante.
    '''

    def __init__(self):
        self.chainepere = None
        self.chainefils = None
        self.retour = False

    def method(self):
        """
        Permet de jouer la methode proposee à ce niveau
        :return: retour de la methode jouée
        """
        self.retour = True
        self._method = self.method
        return self._method()

    @property
    def __hash__(self):
        """
        Le hash est défini en fonction du texte contenu dans l'objet
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