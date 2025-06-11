""" Stop test

**WARNING**: Going to work forever with `create_task`..

If you hit turtleps stop button it should actually stop without errors.

"""

import asyncio 

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


async def main():

    c = 0
    while True:
        print("Counting...", c)
        c += 1
        await asyncio.sleep(1)

if __name__ == '__main__':
    t = asyncio.create_task(main())