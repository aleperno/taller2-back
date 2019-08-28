import random
import string

def random_string(length=10):
    opts = string.ascii_letters + string.digits
    return ''.join(random.choice(opts) for i in range(length))