from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from logging2 import Logger
from urllib.parse import urljoin

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