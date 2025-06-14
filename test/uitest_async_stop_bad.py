""" Stop with bad non-awaited gather test

Bad things will happen if you don't await an asyncio.gather

Pyodide and micropython behavours may differ, but after all it's your fault, isn't it?

See also [test/uitest_async_stop.py](test.html?s=test/uitest_async_stop.py)
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

try:
    # improper use without await, this will still somehow 
    # trigger a CancelledError 
    asyncio.gather(af())   
except BaseException as e:
    print("test: Around gather: I was stopped with BaseException descendant:")
    print_exception(e)
except Exception as e:
    print("test: Around gather: I was stopped with Exception descendant:")
    print_exception(e)

print("test: Going to sleep...")
await asyncio.sleep(5)  # proper use with await, you can safely stop it.
print("test: Woke up...")

print("test: CALLING PROGRAMMATICALLY ge_stop()")
try:
    turtleps.ge_stop()
except BaseException as e:
    tps._info("outside ge_stop: raised:")
    tps.print_exception(e)
except Exception as e:
    tps._info("outside ge_stop: raised:")
    tps.print_exception(e)


print("test: Going to sleep again ...")
await asyncio.sleep(2)
print("test: end of script")