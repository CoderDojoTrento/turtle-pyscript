""" Stop with bad non-awaited gather test

We expect and do want to see asyncio errors.

See also uitest_async_stop.py
"""

import asyncio
import turtleps
import turtleps as tps

async def af():
    c= 0
    while True:
        await asyncio.sleep(0.5)
        tps._debug('c=',c)
        c += 1

try:
    # improper use without await, this will still somehow 
    # trigger an uncatchable CancelledError 
    asyncio.gather(af())   
except BaseException as e:
    print("Around gather: I was stopped:", e)

print("Going to sleep...")
await asyncio.sleep(3)  # proper use with await, you can safely stop it.
print("Woke up...")


try:
    turtleps.ge_stop()
except BaseException as e:
    print("outside ge_stop: raised:", e)

await asyncio.sleep(2)
print("After ge_stop()")