from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

tps._info("TEST SAY DELTA: BEGINNING...")

iarch = 'img/ch-archeologist-e.gif'

screen = Screen()
screen.register_shape(iarch)

await ge_init()

s = Sprite()

s.shape(iarch)

await s.say("abcdefghilmnopqrstuvzABCDEFGHILMNOPQRSTUVZ",2)
await s.say("Higher",2, dy = 120)
await s.say("Lower",2, dy = -120)
await s.say("More right",2, dx = 120)
await s.say("More left",2, dx = -120)

tps._info("TEST SAY DELTA: DONE...")