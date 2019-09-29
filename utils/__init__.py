import random
import string
from datetime import datetime


def random_string(length=10):
    opts = string.ascii_letters + string.digits
    return ''.join(random.choice(opts) for i in range(length))


def utcnow():
    return datetime.utcnow().replace(microsecond=0)
