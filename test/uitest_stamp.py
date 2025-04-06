from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()

iarch = "img/ch-archeologist-e.gif"
screen.register_shape(iarch)

await ge_init()

for i in range(5):
    goto(i*50-150,0)
    stamp()

ada = Sprite()
ada.shape(iarch)

ada.goto(-100,-100)
for i in range(5):
    goto(i*50-150,0)
    ada.stamp()
