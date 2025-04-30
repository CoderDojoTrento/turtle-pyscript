
from turtleps import *

screen = Screen()
screen.bgpic("img/bg-seaside-2.gif")

iarc =  "img/ch-archeologist-e.gif"  # looks east
screen.register_shape(iarc)

iart = "img/ch-arctic-big-e.gif"     # looks east
screen.register_shape(iart)

idino = "img/an-dino-1e.gif"
screen.register_shape(idino)


await ge_init()

ada = Sprite()     # Sprite instead of Turtle
ada.shape(iarc)    # looks east
ada.goto(-100,0)   # move to left side 

bob = Sprite()
bob.shape(iart)           # looks east
bob.shapesize(-1.0,1.0)   # looks left keeping head on top
bob.goto(100,0)

dino = Sprite()
dino.shape(idino)
dino.shapesize(0.7,0.7)
print("ciao")
dino.goto(0,-80)

async def click_dino(evento):
    await dino.say("BAARK!",2)
    await dino.say("GUARK!", 2)
    evento.stopPropagation()

dino.svg.onclick = click_dino


await ada.say("Ciao! Io sono Ada!", 3)
await ada.say("Tu come ti chiami?", 3)
"""
await bob.say("Io sono Bob!", 2)
await bob.say("Mi sono perso!", 3)
await ada.say("Si vede!", 2)
await ada.say("Esploriamo la foresta?", 4)
await bob.say("Ok!", 2)

bob.shapesize(1.0,1.0)    # looks right

await bob.slide(250, 0)   
await ada.slide(250, 0, 2)
"""
dino.hide()
ada.screen.bgpic("img/bg-forest-1.gif")

bob.goto(-200, 0)
ada.goto(-230, 0)

ada.shapesize(1.0, 1.0)  # looks right
bob.shapesize(1.0, 1.0)  # looks right

await asyncio.gather(ada.slide(-100, -0, 2),   
                        bob.slide(100, -0, 2))    

bob.shapesize(-1.0, 1.0)  # looks left

await ada.say("Qua fa più fresco!", 3)
await bob.say("Per me è ancora troppo caldo!", 6)
