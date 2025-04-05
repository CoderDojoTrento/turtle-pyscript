from turtleps import *
import turtleps as tps
from pyscript import document
import asyncio

import sys
tps._info('python version: ', sys.version)


tps._debugging = False
#tps._debugging = True
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

ada.shape("turtle")
bob.shape("arrow")

ada.goto(100,0)
bob.goto(-100,0)


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
    
wt = 0.02

async def move_ada():

    while True:
        # workaround for lag:  https://github.com/CoderDojoTrento/turtle-pyscript/issues/18 
        ada.color('yellow') 

        if "ArrowUp" in keys:
            ada.forward(4)
        if "ArrowLeft" in keys:
            ada.left(5)
        if "ArrowRight" in keys:
            ada.right(5)

        await asyncio.sleep(0.02)  

ada.say("Please click me!", 1)

g = asyncio.gather(update_bob(), 
                   move_ada())


print("STOPPED main")