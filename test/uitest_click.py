
""" Click test

Shows you can click on sprites, background, or anywhere in the whole svg

**Sprites:**  can be clicked by setting `onclick` event

Technical stuff: we don't provide `addEventListener` nor
`stopPropagation` examples to keep things simple, most people
won't need them.

**Background:** 

it's a special sprite always available with `screen.background`, 
depicted here in yellow with its default `"bgpanel"` shape shrinked with `shapesize()`

Technical stuff: If you shrink the background sprite, 
you will end up seeing the main `tps-screen` svg element, here depicted in beige: if you want to listen to clicks on it
just set `onclick` but remember it will always fire alongside with svg elements under it 
(TODO: why??). To change its color just apply css styles.
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
ada.goto(-130,0)


async def click_ada(event):
    tps._info("Clicked ada, event:", event,  c=True)

    await ada.say("You clicked ada!",2)

ada.svg.onclick = click_ada


dino = Sprite()
dino.shape(idino)
dino.shapesize(0.5,0.7)
dino.goto(70,0)

async def click_dino(event):
    tps._info("Clicked dino, event:", event,  c=True)
    await dino.say("You clicked dino",2)
    await dino.say("GUARK!", 2)

dino.svg.onclick = click_dino


donut = Sprite()
donut.shape(idonut)
donut.shapesize(1,1)
donut.goto(70,0)

async def click_donut(event):
    tps._info("Clicked donut, event:", event,  c=True)
    await circles.say("You clicked donut", 2, dx=100, dy = 240)


donut.svg.onclick = click_donut


circles = Sprite()
circles.shape(icircles)
circles.shapesize(1,1)
circles.goto(0,-100)

async def click_circles(event):
    tps._info("Clicked circles, event:", event,  c=True)
    await circles.say("You clicked circles", 2)


circles.svg.onclick = click_circles



async def click_screen_background(event):
    tps._info("Clicked screen.background.svg, event:", event,  c=True)
    
    await screen.background.say("You clicked screen.background.svg", 2, dy=-200)

screen.background.svg.onclick = click_screen_background
screen.background.fillcolor('yellow')
screen.background.shapesize(0.75)


speaker = Sprite()
speaker.goto(0, 180)
speaker.shape('blank')
# notice: this ALWAYS fires, no matter what's inside the svg 
#         Order: first elements fire, then this 
async def click_screen(event):
    tps._info("Clicked (also) screen.svg, event:", event,  c=True)
    
    await speaker.say("You (also) clicked screen.svg", 2)

screen.svg.onclick = click_screen
screen.svg.style.setProperty('background-color', 'beige')
