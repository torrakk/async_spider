from webcrawler.settings import  *
from webcrawler.selenium_parse import *
from pyvirtualdisplay import Display
from selenium import webdriver
import sys
import pytest

# @pytest.fixture
# def display():
#     ecran = Display(visible=BROWSER_VISIBILITY, size=RESOLUTION)
#     ecran.start()
#
# @pytest.fixture()
# def session():
#     session = webdriver.Firefox()
#     session.set_window_size(*RESOLUTION)
#     session.get("https://infinite-scroll.com/demo/full-page/")
#     return session

class webelements():
    def find_elements_by_id(self):
        """Finds a list of elements within this element's children by ID.
        Will return a list of webelements if found, or an empty list if not.

        :Args:
         - id\_ - Id of child element to find.

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_id('foo')
        """

    def find_element_by_id(self):
        """Finds a list of elements within this element's children by ID.
        Will return a list of webelements if found, or an empty list if not.

        :Args:
         - id\_ - Id of child element to find.

        :Returns:
         - WebElement - Element if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_id('foo')
        """

    def click(self):
        """
        click
        :return:
        """
        return None

    def glisse(self):

        return None

#
# def test_windowActionScroll(display, session):
#     print("Début du test window action scroll")
#     display
#     fenetre = windowAction(session)
#     print(fenetre.getHeight())
#     resultat = fenetre.scroll()
#     next(resultat)
#
# def test_windowActionRefresh(display, session):
#     print("Début du test Refresh")
#     display
#     fenetre = windowAction(session)
#     fenetre.refresh()
#     #out, err = capsys.readouterr()

def test_returnItemTypeMulti():
    a = webelements()
    type = getItemType(a.find_elements_by_id)
    assert type == "list"

def test_returnItemTypeSingle():
    a = webelements()
    type = getItemType(a.find_element_by_id)
    assert type == "single"

def test_returnItemForClick():
    a = webelements()
    type = getItemType(a.click)
    assert type == None

def test_returnItemForGlisse():
    a = webelements()
    type = getItemType(a.glisse)
    assert type == None
#
#
# if __name__=="__main__":
#     test_windowActionScroll(display, session)