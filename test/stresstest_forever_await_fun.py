""" Forever while await in a function

**WARNING**: Going to work forever with `create_task` (see console)..


If you hit turtleps stop button:

- **in pyodide**: it should actually stop without errors.
- **in micropython**: it keeps counting because this script doesn't import `turtleps.py`,
    which would allow micropython tasks tracking.  

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