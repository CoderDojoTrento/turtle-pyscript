
from turtleps import *

async def run():

    hideturtle()  # nasconde quella di default

    screen = Screen()
    screen.bgpic("img/bg-seaside-2.gif") 
    screen.register_shape("img/ch-archeologist-e.gif")
    screen.register_shape("img/ch-arctic-big-e.gif")

    await ge_loaded()

    ada = Sprite()                                # Sprite instead of Turtle
    ada.shape("img/ch-archeologist-e.gif")   # looks east
    ada.goto(-100,0)                              # move to left side 

    bob = Sprite()
    bob.shape("img/ch-arctic-big-e.gif")   # looks east
    bob.shapesize(-1.0,1.0)   # looks left keeping head on top
    bob.goto(100,0)


    await ada.say("Ciao! Io sono Ada!", 3)
    await ada.say("Tu come ti chiami?", 3)
    await bob.say("Io sono Bob!", 2)
    await bob.say("Mi sono perso!", 3)
    await ada.say("Si vede!", 2)
    await ada.say("Esploriamo la foresta?", 4)
    await bob.say("Ok!", 2)
    bob.shapesize(1.0,1.0)    # looks right

    for i in range(28):
        bob.goto(bob.x + 5, bob.y)
        await asyncio.sleep(0.05)

    for i in range(65):
        ada.goto(ada.x+5, ada.y)
        await asyncio.sleep(0.02)

    bob.shapesize(-1.0, 1.0)  # looks left
    #bob.goto(250, 0)   # currently immediate
    #ada.goto(250, 0)   # currently immediate

    ada.screen.bgpic("img/bg-forest-1.gif")
    #ada.speed(0)   # currently not supported
    #bob.speed(0)   # currently not supported

    bob.goto(-200, 0)
    ada.goto(-230, 0)
    ada.speed(5)   # normal - currently not supported
    bob.speed(5)   # normal - currently not supported

    bob.shapesize(1.0, 1.0)  # looks right

    for i in range(60):
        bob.goto(bob.x + 5, bob.y)
        await asyncio.sleep(0.05)

    bob.shapesize(-1.0, 1.0)  # looks left

    for i in range(27):
        ada.goto(ada.x + 5, ada.y)
        await asyncio.sleep(0.02)

    #ada.goto(-100, -0)   # currently immediate
    #bob.goto(100, -0)    # currently immediate

    await ada.say("Qua fa più fresco!", 3)
    await bob.say("Per me è ancora troppo caldo!", 6)
