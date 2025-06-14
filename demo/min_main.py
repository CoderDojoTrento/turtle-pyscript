"""Minimal main demo

Some **simple** description
"""

from turtleps import *

screen = Screen()

iseaside = "img/bg-seaside-2.gif"
screen.register_shape(iseaside)

iarc =  "img/ch-archeologist-e.gif"  # looks east
screen.register_shape(iarc)

idino = "img/an-dino-1e.gif"
screen.register_shape(idino)


await ge_init()

screen.background.shape(iseaside)

dino = Sprite()
dino.shape(idino)
dino.shapesize(0.7,0.7)
dino.goto(0,-80)

while True:
    await dino.say("How nice here!", 3)
    await dino.say("I like simple environments!", 3)
