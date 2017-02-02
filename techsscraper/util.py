from dateutil import parser


def clean(data):
    return data.replace('\n', "").replace('\\n', "").strip()


def serialize_date(value):
    return parser.parse(value)

def get_db_name(uri):
    arr = uri.split('/')
    if len(arr) >= 4:
        return arr[3]
