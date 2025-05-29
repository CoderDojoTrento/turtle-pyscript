from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

await ge_init()

ada = Sprite()
ada.shape("turtle")
ada.shapesize(5)
ada.color('green')


bob = Sprite()
bob.shape("square")
bob.shapesize(5)
bob.color('orange')


await asyncio.sleep(1)

ada.to_foreground()

await asyncio.sleep(1)

ada.to_background()