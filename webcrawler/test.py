from webcrawler.settings import  *
from webcrawler.selenium_parse import *
from pyvirtualdisplay import Display
from selenium import webdriver
import sys


def test_windowAction():
    print("Début du test window action")
    display = Display(visible=BROWSER_VISIBILITY, size=RESOLUTION)
    display.start()
    ####
    session = webdriver.Firefox()
    session.set_window_size(*RESOLUTION)
    session.get("https://infinite-scroll.com/demo/full-page/")
    print("La page est chargée")
    fenetre = windowAction(session)
    print(fenetre.getHeight())
    fenetre.scroll()
    print("La hauteur est de " + str(fenetre.newHeight))
    #out, err = capsys.readouterr()

if __name__=="__main__":
    test_windowAction()