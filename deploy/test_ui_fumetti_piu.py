from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

tps._info("TEST FUMETTI: BEGINNING...")
t = Sprite()
t.speed(10)
t.load_image('img/ch-archeologist-e.gif')

await t.say("abcdefghilmnopqrstuvzABCDEFGHILMNOPQRSTUVZ",2)
await t.say("Più in alto",2, dy = 120)
await t.say("Più in basso",2, dy = -120)
await t.say("Più a destra",2, dx = 120)
await t.say("Più a sinistra",2, dx = -120)

tps._info("TEST FUMETTI: DONE...")