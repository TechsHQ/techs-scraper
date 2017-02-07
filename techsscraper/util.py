import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def get_db_name(uri):
    arr = uri.split('/')
    if len(arr) >= 4:
        return arr[len(arr) - 1]


def sanatize_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://%s' % url
    return url


def fix_url(url, domain):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = url.replace('//', '')
        if '.' in url:
            url = '/' + url.split('/', 1)[-1]
        url = domain + url
    return url


def get_domain(url):
    return '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
