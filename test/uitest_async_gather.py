""" Async gather test

Shows complex event management with asyncio.gather primitive 

**in pyodide (default):** It should be stoppable and replayable without problems

**in micropython:**  

- if you stop _before_ Mr Egg ends the fall, everything behaves as expected
- if you stop _after_ Mr Egg ends the fall, then the `move_ada` task events are unregistered 
but function is not stopped. This is strange because in the example we do properly catch Mr Egg exception 

"""


from turtleps import *
import turtleps as tps
from pyscript import document
import asyncio

import sys
tps._info('python version: ', sys.version)


#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

# await resources
await ge_init()

# handle keys

keys = set()

def keydown(event):
    print("keydown", event.key)
    keys.add(event.key)

def keyup(event):
    print("keyup", event.key)
    if event.key in keys:
        keys.remove(event.key)

document.onkeydown = keydown
document.onkeyup = keyup


# do the rest

screen = Screen()

ada = Sprite()
bob = Sprite()
egg = Sprite()   # will break

ada.shape("turtle")
bob.shape("arrow")
egg.shape("triangle")

ada.goto(100,0)
bob.goto(0,0)
egg.goto(-100,0)

async def click_ada(event):
    print("event:", event)
    await ada.say("You clicked me...!", 2)
    await ada.say("Nice job!", 2)

# pyscript 2025.3.1 : works in cpython, doesn't  in micropython 
ada.svg.onclick = click_ada

async def update_bob():
    while True:
        await bob.slide(0,100,3)
        await bob.slide(0,-100,3)


async def update_egg():
    await egg.slide(-100,-150,1)
    egg.setheading(90)
    raise Exception("Mr Egg was broken!")


    
wt = 0.02

async def move_ada():

    while True:
        await asyncio.sleep(0.02)

        # workaround for lag:  https://github.com/CoderDojoTrento/turtle-pyscript/issues/18 
        ada.color('black') 

        if "ArrowUp" in keys:
            ada.forward(4)
        if "ArrowLeft" in keys:
            ada.left(5)
        if "ArrowRight" in keys:
            ada.right(5)
          

ada.say("Please click me!", 1)

b = update_bob()  # assigning doesn't complain about missed await
a = move_ada()
e = update_egg()

async def click_egg(event):
    await egg.say("You clicked me!", 2)  # TODO put some logging message about tasks state
    
# pyscript 2025.3.1 : works in cpython, doesn't  in micropython 
egg.svg.onclick = click_egg


g = asyncio.gather(b,                
                   e,
                   a)
tps._info("gather in progress: ", g)

try:
    await g
except Exception as e:
    print("TEST: Caught gather Exception descendant:")
    print_exception(e, file=sys.stdout)
    
except BaseException as e:
    print("TEST: Caught gather BaseException descendant:")
    print_exception(e, file=sys.stdout)
tps._info("End of uitest_event_loop")