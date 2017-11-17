from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError

from urllib.parse import urljoin

def joinUrl(*args):
    return urljoin(*args)


def validateUrl(url):
    val = URLValidator()
    email = EmailValidator()
    try:
        val(url)
        if 'mailto' not in url:
            return True
        else:
            return
    except(ValidationError):
        return

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