
from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False
 

screen = Screen()

idino = "img/an-dino-1e.gif"
iturtle = "img/turtle.svg"
inonexisting1 = "bad-address.gif"
inonexisting2 = "wrong-address.gif"


screen.register_shape(iturtle)
screen.register_shape(idino)
screen.register_shape(inonexisting1)
screen.register_shape(inonexisting2)

tps._info("Testing shape usage too soon, expect wrong size:")
shape = Screen()._shapes[idino]
tps._info(f"  - registered shape: {shape}")
tps._info(f"    - shape size: {shape.get_svg_image_size()}")


tps._info("Testing shape usage too soon, expect wrong size:")
shape = Screen()._shapes[inonexisting1]
tps._info(f"  - registered shape: {shape}")
tps._info(f"    - shape size: {shape.get_svg_image_size()}")


tps._info("Now calling ge_init()...")

await ge_init()


ada = Sprite()
ada.shape(iturtle)
ada.shapesize(0.7,0.7)
ada.goto(-100,0)

dino = Sprite()
dino.shape(idino)
dino.shapesize(0.7,0.7)
dino.goto(100,0)

bad = Sprite()
bad.shape(inonexisting1)
bad.goto(0,-100)


nasty = Sprite()
nasty.shape(inonexisting2)
nasty.goto(0,100)




