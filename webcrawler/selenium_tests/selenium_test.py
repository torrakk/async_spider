import re, itertools
from selenium import webdriver
from bs4 import BeautifulSoup as BS

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def main():
    from selenium.webdriver import Firefox, Chrome
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time


    opts = Options()
    opts.add_argument("--headless")
    browser = Firefox(options=opts)
    browser.maximize_window()
    print("debut du chargement")
    browser.get('https://bandcamp.com')
    print("nous cherchons l'élement")
    element = WebDriverWait(browser, 0).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "playbutton")))
    print("l\'élement est chargé")
    browser.find_element_by_class_name('playbutton').click()
    time.sleep(50)
    print("Nous quittons blam !!")
    browser.quit()



    # driver = webdriver.Firefox()
    # print("la fenêtre est lancée")
    # #driver.set_window_size(1400,1000)
    # driver.get("https://www.pinterest.com/search/pins/?q=old")
    #
    # buttons = driver.find_elements_by_xpath('//button[@data-test-id="seemoretoggle"]');
    # for btn in buttons:
    #     btn.click()
    #
    # html = driver.page_source
    # soup = BS(html, 'html.parser')
    # elem = soup.find(string=re.compile('Tiny House interior'))
    # print(elem)
    # xpath_soup(elem)
    # print(xpath_soup(elem))

if __name__ == '__main__':
    main()