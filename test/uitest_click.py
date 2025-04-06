
from turtleps import *
import turtleps as tps


#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

idino = "img/an-dino-1e.gif"
iturtle = "img/turtle.svg"

screen.register_shape(idino)
screen.register_shape(iturtle)

await ge_init()


ada = Sprite()
ada.shape(iturtle)
ada.shapesize(0.7,0.7)
ada.goto(-100,0)

dino = Sprite()
dino.shape(idino)
dino.shapesize(0.7,0.7)
dino.goto(100,0)


async def click_ada(event):
    await ada.say("You clicked me!",2)
    #event.stopPropagation()

ada.svg.onclick = click_ada


async def click_dino(evento):
    await dino.say("BAARK!",2)
    await dino.say("GUARK!", 2)

dino.svg.onclick = click_dino


