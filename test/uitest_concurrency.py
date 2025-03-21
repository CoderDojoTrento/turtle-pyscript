from turtleps import *
import turtleps as tps
import time

import sys
tps._info('python version: ', sys.version)

import pyodide
print("pyodide:", pyodide.__version__)

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

    

ge_tasks = []


class CdtnAwait:
    """A wrapper for functions that could be both sync and async"""
    
    def __init__(self, f, *args, **kwargs) -> None:
        self._f = f
        self._args = args
        self._kwargs = kwargs
        

    def __call__(self, *args, **kwargs) -> None:
        
        tps._debug("CdtnAwait.__call__")        
        t = asyncio.create_task(self._f(*self._args, **self._kwargs))
        ge_tasks.append(t) # for not losing reference??
        
    def __await__(self): #-> Generator[None, None, None]:
        tps._debug("CdtnAwait.__await__")
        async def my_await() -> None:
            #if self._f:                
            t = asyncio.create_task(self._f(*self._args, **self._kwargs), name="await mount")    
            await asyncio.wait([t])
                    
        return my_await().__await__()
    
def slideB(sprite : Sprite, x, y, seconds : float):
    c = CdtnAwait(Sprite.slide, sprite, x,y, seconds)
    return c()

    

await ge_init()

screen = Screen()


ada = Sprite()
bob = Sprite()
ada.color('pink')
ada.shape('turtle')
bob.shape('arrow')

ts = time.time()
"""
tps._info("Testing class CdtnAwait WITH await")
tps._info("Resetting..")
ada.goto(0,0)
bob.goto(0,0)

tps._info("  Ada goes awaiting with class CdtnAwait...!")
await slideB(ada, 100, 100, 3)
tps._info("  ada slideB done!")
tps._info("  Bob goes awaiting with class CdtnAwait...!")
await slideB(bob, -100, 100, 3)
tps._info("  bob slideB done!")

"""
tps._info("Testing class CdtnAwait WITHOUT await")
tps._info("Resetting..")
ada.goto(0,0)
bob.goto(0,0)

tps._info("Ada goes without awaiting with class magic...!")
slideB(ada, 0, 100, 3)
tps._info("ada slideB done!")
tps._info("Bob goes without awaiting with class magic...!")
slideB(bob, 0, -100, 3)
tps._info("bob slideB done!")

color('green')
write('Sudden change!')

"""

tps._info("Testing simple async slideA...!")
tps._info("Should be blocking...")

tps._info("Ada goes sequentially...!")
await slideA(ada, -100, 100, 3)
te = time.time()
tps._info("Elapsed time", te-ts)
await slideA(ada, 0, 0, 3)

tps._info("Testing simple async slideA gather...!")
tps._info("Should be NON-blocking...")

tps._info("Now Ada and Bob together!")
asyncio.gather(slideA(ada, 0, 100, 4), 
               slideA(bob, 0, -100, 2))
color('green')
write('Sudden change!')

"""