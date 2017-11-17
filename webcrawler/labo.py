from bs4 import BeautifulSoup
import re
def generateur(list, pas):
    start = 0
    end = 0
    while end < len(list):
        end = start + pas
        yield list[start:end]
        start = end

list = [i for i in range(1,8001)]
# parseDemiList()
# listing = itertools.islice(list, 1, len(list),10)
# listtt = []
for i in generateur(list, 2):
    print(i)



page = 'https://www.data.gouv.fr/fr/search/?tag=haute-loire'
soup = BeautifulSoup(page, 'html.parser')
recherche = soup.find_all('a', attrs={'string': re.compile('servitude')})
print(recherche)