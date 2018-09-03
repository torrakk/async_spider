from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from logging2 import Logger
from urllib.parse import urljoin
import bs4
from webcrawler.static_page.page_test import html

def joinUrl(*args):
    return urljoin(*args)


def validateUrl(*urls):
    val = URLValidator()
    email = EmailValidator()
    for url in urls:
        try:
            val(url)
            if 'mailto' not in url:
                yield url
        except(ValidationError, AttributeError):
            continue
            #print('Nous avons une erreur de validation d\'url {}'.format(url))

def reorgPaquetGenerator(list, pas):
    if pas == 0:
        pas = 1
    start = 0
    end = 0
    pas = int(len(list)/pas)
    while end <= len(list):
        end = start + pas
        yield list[start:end]
        start = end


def xpath(func):
    def xpath_soup(*args):
        element_liste = func(*args)
        for element in element_liste:
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
            attrs = getattr(element, 'attrs', {})
            attrs.update({'xpath': '/%s' % '/'.join(components)})
            # print("Nous avons ajouté le xpath {}".format(components))
        return element_liste
    return xpath_soup

if __name__=="__main__":

    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>
    
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    
    <p class="story">...</p>
    </body>
    <html>
    """
    #.portail-gauche > div:nth-child(2) > ul:nth-child(3) > li:nth-child(1) > time:nth-child(1)
    soup = bs4.BeautifulSoup(html.replace("\n", "").replace("\t", ""), 'lxml-xml')
    atttr = soup.find('time')
    #print(atttr)
    print(xpath(atttr))