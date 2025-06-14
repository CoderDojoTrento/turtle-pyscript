""" Stop test with properly awaited gather 

Automatically stops by calling `ge_stop()` after a 3 seconds

Should work both in pyodide and micropython

Note to really stop pyodide it would need to be [in a worker](
https://pyodide.org/en/stable/usage/keyboard-interrupts.html)

TODO CHECK: 
https://stackoverflow.com/questions/73051054/python-threading-how-to-interrupt-the-main-thread-and-make-it-do-something-else
"""

import asyncio
import turtleps
import turtleps as tps

async def af():
    c= 0
    while True:
        await asyncio.sleep(1)
        tps._info('c=',c)
        c += 1

async def sleeper():
    print("Going to sleep...")
    await asyncio.sleep(3) 
    print("Woke up...")
    turtleps.ge_stop()

try:
    await asyncio.gather(af(), sleeper())   
except BaseException as e:
    tps._info("During gather: I was stopped with", e.__class__.__name__,":", e )