""" Danger forever with while / await

"""

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


import asyncio 

eprint("WARNING: Going to work forever with while /await..")
eprint("")
eprint("If you hit turtleps stop button it should actually stop without errors.")

c = 0
while True:
    print("Counting...", c)
    c += 1
    await asyncio.sleep(1)
