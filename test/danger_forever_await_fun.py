""" Stop test

"""
import asyncio 

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


async def main():
    eprint("WARNING: Going to work forever with create_task..")
    eprint("")
    eprint("If you hit turtleps stop button it should actually stop without errors.")

    c = 0
    while True:
        print("Counting...", c)
        c += 1
        await asyncio.sleep(1)

if __name__ == '__main__':
    t = asyncio.create_task(main())