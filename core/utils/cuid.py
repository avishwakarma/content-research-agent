from cuid2 import Cuid

# create a cuid map for length
cuid_map = {}


def cuid(length: int):
    return Cuid(length=length).generate(length=length)
