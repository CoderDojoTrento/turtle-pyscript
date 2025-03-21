from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

tps._info("TEST FUMETTI CIAO: BEGINNING...")
t = Sprite()
t.speed(10)
t._load_image('img/ch-archeologist-e.gif')

await t.say("Ciao1", 1)
t.goto(-250, 0)
await t.say("Ciao2", 1)
t.goto(250, 0)
await t.say("Ciao3", 1)
t.goto(0, 250)
await t.say("Ciao4", 1)
t.goto(0, -250)
await t.say("Ciao5", 1)
t.goto(250, -250)
await t.say("Ciao6", 1)
t.goto(-250, 250)
await t.say("Ciao7", 1)
t.goto(-250, -250)
await t.say("Ciao8", 1)
t.goto(250, 250)
await t.say("Ciao9", 1)

tps._info("TEST FUMETTI CIAO: DONE...")