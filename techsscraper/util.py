from urllib.parse import urlparse


def get_db_name(uri):
    arr = uri.split('/')
    if len(arr) >= 4:
        return arr[len(arr) - 1]


def sanatize_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://%s' % url
    return url


def get_domain(url):
    return '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
