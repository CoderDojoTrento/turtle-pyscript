
""" Click test

Shows you can click screen or sprites
"""

from turtleps import *
import turtleps as tps
import inspect 

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

idino = "img/an-dino-1e.gif"
iturtle = "img/turtle.svg"
idonut = "test/img/donut.svg"
icircles = "test/img/2circles.svg"

screen.register_shape(idino)
screen.register_shape(iturtle)
screen.register_shape(idonut)
screen.register_shape(icircles)


await ge_init()


ada = Sprite()
ada.shape(iturtle)
ada.shapesize(0.7,1.2)
ada.goto(-100,0)


async def click_ada(event):
    tps._info("Clicked ada, event:", event,  c=True)

    await ada.say("You clicked me!",2)

ada.svg.onclick = click_ada


dino = Sprite()
dino.shape(idino)
dino.shapesize(0.5,0.7)
dino.goto(100,0)

async def click_dino(event):
    tps._info("Clicked dino, event:", event,  c=True)
    await dino.say("BAARK!",2)
    await dino.say("GUARK!", 2)

dino.svg.onclick = click_dino


donut = Sprite()
donut.shape(idonut)
donut.shapesize(1,1)
donut.goto(100,0)

async def click_donut(event):
    tps._info("Clicked donut, event:", event,  c=True)
    
donut.svg.onclick = click_donut


circles = Sprite()
circles.shape(icircles)
circles.shapesize(1,1)
circles.goto(0,-100)

async def click_circles(event):
    tps._info("Clicked circles, event:", event,  c=True)
    
circles.svg.onclick = click_circles



# notice: first this fires, then event is caught by elements 
def click_screen(event):
    tps._info("Clicked screen, event:", event,  c=True)

screen.svg.onclick = click_screen

