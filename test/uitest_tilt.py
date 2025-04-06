from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

screen = Screen()
screen.register_shape('img/turtle.svg')

await ge_init()

ada = Turtle()
bob = Turtle()


ada.shape('img/turtle.svg')
heading_before = ada.heading()

await asyncio.sleep(0.5)
ada.tilt(40)
assert heading_before == ada.heading()

for i in range(4):
    await asyncio.sleep(0.5)
    ada.forward(100)
    await asyncio.sleep(0.5)
    ada.left(90)


await asyncio.sleep(0.5)
bob.tilt(-40)
bob.setheading(-90)
assert heading_before == ada.heading()

await asyncio.sleep(0.5)
bob.forward(100)
await asyncio.sleep(0.5)
bob.left(90)
await asyncio.sleep(0.5)
bob.forward(100)