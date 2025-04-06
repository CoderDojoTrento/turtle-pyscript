from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False


tps._info("TEST TURTLEPS: BEGINNING...")

ada = Sprite()

ada.screen.register_shape('img/turtle.svg')

await ge_init()

ada.shape('img/turtle.svg')

print("shapesize:", ada.shapesize())
#for i in range(3):
ada.color('green')
ada.shapesize(0.3,0.5)
print("shapesize:", ada.shapesize())

await ada.say("Ciao!", 3)


ada.write("Ciao mondo!", align="right", font=("Courier", 18, "bold"))
ada.forward(100)
#time.sleep(1)
#await asyncio.sleep(1)

ada.left(90)

#time.sleep(1)

ada.dot(40)

ada.forward(100)
ada.color('blue')

ada.circle(20)
ada.write("La la", align="center", font=("Times New Roman", 24, "italic"))
ada.left(90)
ada.forward(100)

tps._info("TEST TURTLEPS: DONE...")
