import logging
import pytz
from dateutil import parser

logger = logging.getLogger(__name__)


def clean(data):
    return data.replace('\n', "").replace('\t', "").replace('\\n', "").strip()


def parse_date(t):
    return parser.parse(t).astimezone(pytz.timezone('UTC'))


def check_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        logger.warning('Invalid url: %s', url)
        return 'http://' + url
    return url
