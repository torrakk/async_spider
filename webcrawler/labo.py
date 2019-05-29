from bs4 import BeautifulSoup
import re
import urllib3
from operator import xor

# nomfichier = re.compile('(?P<nomfichier>.*)')
# fichier = 'attachment; filename="AssiettesdeservitudeEL3lieeaux.zip"'
# print(nomfichier.search(fichier))


# def dataSearch(data):
#     '''
#     Fait une recherche des données resultats pour les injecter dans les datas
#     envoyées lors du post
#     :param data:
#     :param datasearch:
#     :return:
#     '''
#     # 1 va chercher la données à reprendre
#     reg = re.compile('^init:(.*)')
#     recherche = { reg.match(datakeys).group(1):values for datakeys, values in data.items() if reg.match(datakeys)}
#     print(recherche)
#     # if recherche:
#     #     return xor(recherche, data)
#     return
#
#
# data = {'quatre':'test', 'init:test': 'valeure'}
#
# print(dataSearch(data))

DOCSTRING_LIST_WEBELEMENT = re.compile('^.*:Returns:.*- (list of WebElement).*$')
DOCSTRING_WEBELEMENT = re.compile('^.*:Returns:.*- (WebElement).*$')
TEXT = '''        Finds elements by class name.

        :Args:
         - name: The class name of the elements to find.

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = driver.find_elements_by_class_name('foo')'''

def getDocstring(element=None):
    element = element.__doc__.replace("\n", '')
    print(element)
    heu = DOCSTRING_LIST_WEBELEMENT.match(element)
    ha = DOCSTRING_WEBELEMENT.match(element)
    print(ha, heu)
    return any([ha, heu])


from selenium import webdriver
browser = webdriver.Firefox()

print(getDocstring(browser._web_element_cls.click))
print(getDocstring(browser.find_elements_by_class_name))
# getDocstring(TEXT)
# browser.close()
# def generateur(list, pas):
#     start = 0
#     end = 0
#     while end < len(list):
#         end = start + pas
#         yield list[start:end]
#         start = end

# list = [i for i in range(1,8001)]
# # parseDemiList()
# # listing = itertools.islice(list, 1, len(list),10)
# # listtt = []
# for i in generateur(list, 2):
#     print(i)


#
# url = 'https://www.data.gouv.fr/fr/search/?tag=haute-loire'
# # http = urllib3.PoolManager()
# http = urllib3.PoolManager()
# r = http.request('GET', url)
# page = r.data
# soup = BeautifulSoup(page, 'html.parser')
# recherche = soup.find_all(href=re.compile('servitude'))
# print(recherche)