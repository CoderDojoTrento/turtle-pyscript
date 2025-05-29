""" Empty background test

A background is a special default Sprite

When it's empty, it should have bgpanel shape, white color,
and screen width and height.

The donut should go to -200, 100 coords.

"""

from turtleps import *
import turtleps as tps
 

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

idonut = "test/img/donut.svg"

screen.register_shape(idonut)

await ge_init()


donut = Sprite()
donut.shape(idonut)
donut.shapesize(0.3)
donut.goto(0,0)
donut.pendown()
donut.goto(-200, 100)

async def click_donut(event):
    tps._info("Clicked donut, event:", event,  c=True)
    
donut.svg.onclick = click_donut