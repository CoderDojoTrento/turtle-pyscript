""" Memory eater test

"""

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("WARNING: Going to eat RAM forever, expect MemoryError ...")

lst = ['a']*10

while True:
    lst += lst * 2