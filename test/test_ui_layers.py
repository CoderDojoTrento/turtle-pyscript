from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

ada = Sprite()
ada.load_image("img/ch-archeologist-e.gif")

bob = Sprite()
bob.load_image("img/ch-arctic-big-w.gif")

await asyncio.sleep(1)

ada.to_foreground()

await asyncio.sleep(1)

ada.to_background()