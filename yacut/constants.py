import string

SYMBOLS = string.ascii_letters + string.digits
LENGTH_STRING = 6
LINK_REGEX = r'^[a-zA-Z\d]{1,16}$'
FIELD_NAMES = {'original': 'url', 'short': 'custom_id'}