from bs4 import BeautifulSoup
import re
import urllib3
from operator import xor

# nomfichier = re.compile('(?P<nomfichier>.*)')
# fichier = 'attachment; filename="AssiettesdeservitudeEL3lieeaux.zip"'
# print(nomfichier.search(fichier))


def dataSearch(data):
    '''
    Fait une recherche des données resultats pour les injecter dans les datas
    envoyées lors du post
    :param data: 
    :param datasearch: 
    :return: 
    '''
    # 1 va chercher la données à reprendre
    reg = re.compile('^init:(.*)')
    recherche = { reg.match(datakeys).group(1):values for datakeys, values in data.items() if reg.match(datakeys)}
    print(recherche)
    # if recherche:
    #     return xor(recherche, data)
    return


data = {'quatre':'test', 'init:test': 'valeure'}

print(dataSearch(data))
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