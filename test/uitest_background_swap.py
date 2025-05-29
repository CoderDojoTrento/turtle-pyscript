""" Background swap test

Tests background image swap and flashing.

The donut should go to -200, 100 coords.

Verifies:

- drawing pen
- resizing (background clicks outside visible image are ignored by design)

STILL TODO:

- flashing
- drawing on translated
- drawing on rotated
- drawing on resized
"""

from turtleps import *
import turtleps as tps
 

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

idonut = "test/img/donut.svg"
ibg1 = "img/bg-forest-1.gif" 
ibg2 = "test/img/bg-leaves.jpg" 

screen.register_shape(ibg1)
screen.register_shape(ibg2)
screen.register_shape(idonut)

await ge_init()

bg = screen.background

bg.shape(ibg1)

donut = Sprite()
donut.shape(idonut)
donut.shapesize(0.3)
donut.goto(0,0)
donut.pencolor('pink')
donut.pensize(3)
donut.pendown()
donut.goto(-200, 100)

async def click_bg(event):
    tps._info("Clicked background, event:", event,  c=True)
    if bg.shape() == ibg1:
        bg.shape(ibg2)
        bg.shapesize(0.3)
    else:
        bg.shape(ibg1)
        bg.shapesize(1.0)
        
bg.svg.onclick = click_bg

await bg.say("Click me to swap background!", 100, dy=150)