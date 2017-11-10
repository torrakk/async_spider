from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from urllib.parse import urljoin

def joinUrl(*args):
    return urljoin(*args)


def validateUrl(url):
    val = URLValidator()
    try:
        val(url)
        return True
    except(ValidationError):
        return
