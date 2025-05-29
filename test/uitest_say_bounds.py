from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

tps._info("TEST SAY BOUNDS: BEGINNING...")

iarch = 'img/ch-archeologist-e.gif'

screen = Screen()
screen.register_shape(iarch)

await ge_init()


s = Sprite()
s.pendown()
s.shape(iarch)

await s.say("Ciao1", 1)
s.goto(-250, 0)
await s.say("Ciao2", 1)
s.goto(250, 0)
await s.say("Ciao3", 1)
s.goto(0, 250)
await s.say("Ciao4", 1)
s.goto(0, -250)
await s.say("Ciao5", 1)
s.goto(250, -250)
await s.say("Ciao6", 1)
s.goto(-250, 250)
await s.say("Ciao7", 1)
s.goto(-250, -250)
await s.say("Ciao8", 1)
s.goto(250, 250)
await s.say("Ciao9", 1)
tps._info("TEST SAY BOUNDS: DONE...")