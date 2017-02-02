from dateutil import parser


def clean(data):
    return data.replace('\n', "").replace('\\n', "").strip()


def serialize_date(value):
    return parser.parse(value)
