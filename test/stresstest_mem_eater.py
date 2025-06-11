""" Memory eater test

**WARNING**: Going to eat RAM forever, expect MemoryError ...


"""

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

lst = ['a']*10

while True:
    lst += lst * 2