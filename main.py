from turtleps import *
from pyscript import document

screen = Screen()
ispazio = "img/bg-space-1.gif"
irazzo = "img/vh-rocket-1ut.gif"
istella = "img/ob-energy.gif"

screen.bgpic(ispazio) 
screen.register_shape(irazzo)
screen.register_shape(istella)

await ge_init()


rocket = Sprite()
rocket.shape(irazzo)  # rocket guarda in su
rocket.pensize(5)
rocket.pendown()
rocket.tilt(-90)      # aggiustiamo l'orientamento finchè l'*immagine* guardi a destra

stella = Sprite()
stella.shape(istella)
stella.goto(-130,130)


tasti = set()

def tasto_down(evento):
    tasti.add(evento.key)

def tasto_up(evento):
    if evento.key in tasti:
        tasti.remove(evento.key)

document.onkeydown = tasto_down
document.onkeyup   = tasto_up

attesa = 0.02

async def muovi_stella():
    while True:
        await stella.slide(-130, 110, 1)
        await stella.slide(-130, 90, 1)

async def muovi_razzo():

    while True:
        # workaround per il lag:  https://github.com/CoderDojoTrento/turtle-pyscript/issues/18 
        rocket.color('yellow') 

        if "ArrowUp" in tasti:
            rocket.forward(4)
        if "ArrowLeft" in tasti:
            rocket.left(5)
        if "ArrowRight" in tasti:
            rocket.right(5)

        await asyncio.sleep(attesa)  # ATTENZIONE all'indentazione!

async def scopri():

    while True:

        if rocket.x < -100 and rocket.y > 100:
            await rocket.say("Hai trovato una nuova stella!", 2) 
        
        await asyncio.sleep(attesa)   # ATTENZIONE all'indentazione!


await rocket.say("Use arrow keys!", 2)

asyncio.gather(muovi_stella(), 
               muovi_razzo(),
               scopri())

