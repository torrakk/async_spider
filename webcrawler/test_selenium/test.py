from webcrawler.settings import  *
from webcrawler.selenium_parse import *
from selenium import webdriver


def test_windowAction():
    from pyvirtualdisplay import Display
    display = Display(visible=BROWSER_VISIBILITY, size=RESOLUTION)
    display.start()
    ####
    session = webdriver.Firefox()
    session.set_window_size(*RESOLUTION)
    session.get("https://infinite-scroll.com/demo/full-page/")
    fenetre = windowAction(session)
    assert fenetre.scroll()[0] == True