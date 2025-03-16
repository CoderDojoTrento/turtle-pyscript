from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

for i in range(5):
    goto(i*50-150,0)
    stamp()

ada = Sprite()
ada.load_image("img/ch-archeologist-e.gif")
ada.goto(-100,-100)
for i in range(5):
    goto(i*50-150,0)
    ada.stamp()
