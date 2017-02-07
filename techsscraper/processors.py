import pytz
from dateutil import parser


def clean(data):
    return data.replace('\\n', "").strip('\n\t')


def parse_date(t):
    return parser.parse(t).astimezone(pytz.timezone('UTC'))
