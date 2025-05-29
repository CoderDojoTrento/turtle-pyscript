
""" Async stress test

**Red triangle WARNING:** runs a loop that swaps 1000 images without
yealding with `asyncio.sleep`. It will run all the code immediately
and show only the last one..

BUT:

even if Python ends the computation quickly, Chrome engine keeps
itself superbusy for garbage collector stuff I guess, preventing UI
from receiving user input.

**Green turtle**: runs same loop with a small `asyncio.sleep`: will be slow at cycling, but 
at least UI remains alive.

**SO JUST USE `ASYNCIO.SLEEP**

"""

from turtleps import *
import turtleps as tps
 

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

idonut = "test/img/donut.svg"
ibg1 = "img/bg-seaside-2.gif"
ibg2 = "test/img/bg-leaves.jpg" 
ibg3 = "img/bg-forest-1.gif"

screen.register_shape(ibg1)
screen.register_shape(ibg2)
screen.register_shape(ibg3)
screen.register_shape(idonut)

await ge_init()

bg = screen.background

bg.shape(ibg1)


ada = Sprite()
ada.shape("turtle")
ada.color("green")
ada.shapesize(3)
ada.goto(100, 0)

async def click_ada(event):
    tps._info("Clicked ada, event:", event,  c=True)
    print("Going to slow down ui....")

    bg.shape(ibg2)

    for i in range(1,1001):
        tps._info("i=", i)
        await asyncio.sleep(0.01)  # you *REALLY* want to place this
        if bg.shape() == ibg1:
            bg.shape(ibg2)
            bg.shapesize(0.4)
        else:
            bg.shape(ibg1)
            bg.shapesize(1.0)

    bg.shape(ibg3)
    bg.shapesize(1.0)

ada.svg.onclick = click_ada


circle = Sprite()
circle.shape("circle")
circle.shapesize(3)
circle.goto(0,0)
circle.color('blue')
circle.pensize(8)
circle.pendown()
circle.goto(0, 150)


async def circle_run():
    while True:
        await asyncio.sleep(1)
        await circle.say("I'm alive!", 0.5)


async def click_circle(event):
    tps._info("Clicked circle, event:", event,  c=True)
    await circle.say("You clicked me!", 1)

circle.svg.onclick = click_circle


triangle = Sprite()
triangle.shape("triangle")
triangle.color("red")
triangle.shapesize(3)
triangle.goto(-100, 0)

async def click_triangle(event):
    tps._info("Clicked triangle, event:", event,  c=True)
    print("Going to block ui....")

    bg.shape(ibg2)

    for i in range(1,1001):
        tps._info("i=", i)
        #await asyncio.sleep(0.01)  # you *REALLY* want to place this
        if bg.shape() == ibg1:
            bg.shape(ibg2)
            bg.shapesize(0.4)
        else:
            bg.shape(ibg1)
            bg.shapesize(1.0)

    bg.shape(ibg3)
    bg.shapesize(1.0)


triangle.svg.onclick = click_triangle



await asyncio.gather(circle_run(), 
                     triangle.say("  BURN CPU  ", 1000),
                     ada.say("  EPILEPSY WARNING  ", 1000))

