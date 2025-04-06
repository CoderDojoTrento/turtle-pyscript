from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()
iarch = "img/ch-archeologist-e.gif"
screen.register_shape(iarch)

iartic = "img/ch-arctic-big-e.gif"
screen.register_shape(iartic)

await ge_init()

ada = Sprite()
ada.shape(iarch)

bob = Sprite()
bob.shape(iartic)

await asyncio.sleep(1)

ada.to_foreground()

await asyncio.sleep(1)

ada.to_background()