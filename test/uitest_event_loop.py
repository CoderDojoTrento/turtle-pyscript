from turtleps import *
import turtleps as tps
from pyscript import document

import sys
tps._info('python version: ', sys.version)

#import pyodide
#print("pyodide:", pyodide.__version__)

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

# await resources
await ge_init()



# handle keys

keys = set()

def keydown(evento):
    keys.add(evento.key)

def keyup(event):
    if event.key in keys:
        keys.remove(event.key)

document.onkeydown = keydown
document.onkeyup   = keyup

# do the rest

screen = Screen()

ada = Sprite()
bob = Sprite()

ada.shape("turtle")
bob.shape("arrow")

ada.goto(100,0)
bob.goto(-100,0)


async def handle_mouse(e):
    print("event:", e)
    await ada.say("You clicked me...!", 2)
    await ada.say("Nice job!", 2)

ada.svg.onclick = handle_mouse

async def update_bob():
    while True:
        await bob.slide(0,100,3)
        await bob.slide(0,-100,3)
    
wt = 0.02

async def move_ada():
    
    while True:
        if e.key == "ArrowRight":
            ada.x += 3
        if e.key == "ArrowLeft":
            ada.x -= 3
        if e.key == "ArrowUp":
            ada.y -= 3
        if e.key == "ArrowDown":
            ada.y -= 3

        await asyncio.sleep(0.02)  # REMEMBER the await!

ada.say("Please click me!", 1)

g = asyncio.gather(update_bob(), 
                   move_ada())
