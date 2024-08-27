from turtleps import *

#_debugging = False
_debugging = True
#_tracing = True
_tracing = False

def _debug(*args):
    if _debugging:
        print("DEBUG:",*args)

def _trace(*args):
    if _tracing:
        print("TRACE:",*args)
        
def _info(*args):
    print("INFO:", *args)

def _warn(*args):
    print("WARN:", *args)


async def test_turtleps():
    _info("TEST TURTLEPS: BEGINNING...")
    
    ada = Turtle()

    ada.screen.register_shape('img/turtle.svg')
    ada.shape('img/turtle.svg')

    #await asyncio.sleep(1)

    print("shapesize:", ada.shapesize())
    #for i in range(3):
    ada.color('green')
    ada.shapesize(3,15.7)
    print("shapesize:", ada.shapesize())
    
    await dire(ada, "Ciao!", 3)


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
    
    _info("TEST TURTLEPS: DONE...")



async def test_shapesize_one():
    arc = 'img/ch-archeologist-e.gif'
    screen = Screen()
    screen.register_shape(arc)
    #hideturtle()
    shape(arc)
    color('green')
    dot(5)
    shapesize(2.0)
    

async def test_shapesize_many():
    arc = 'img/ch-archeologist-e.gif'
    tsvg = 'img/turtle.svg'
    screen = Screen()
    screen.register_shape(arc)
    screen.register_shape(tsvg)
    

    a = Turtle(shape=arc)
    a.up()
    a.goto(-150,0)
    a.down()
    a.color('green')
    a.dot(5)
    #a.shapesize(1.0)

    b = Turtle(shape=arc)
    b.up()
    b.goto(-100,0)
    b.down()
    b.color('red')
    b.dot(5)
    b.shapesize(2.0)

    c = Turtle(shape=arc)
    c.up()
    c.goto(0,0)
    c.down()
    c.color('blue')
    c.dot(5)

    c.shapesize(1.0, 2.0)

    d = Turtle(shape=arc)
    d.up()
    d.goto(50,0)
    d.shapesize(0.5)

    e = Turtle(shape=arc)
    e.up()
    e.goto(100,0)
    e.shapesize(2.0,1.0)

    p = Turtle(shape=tsvg)
    p.up()
    p.down()
    p.color('lime')
    p.dot(5)
    p.goto(-100,200)
    #p.shapesize(1.0,1.0)

    q = Turtle(shape=tsvg)
    q.up()
    q.goto(100,200)
    q.down()
    q.color('pink')
    q.dot(5)
    q.shapesize(-1.0,1.0)

    r = Turtle(shape=tsvg)
    r.up()
    r.goto(-100,-200)
    r.down()
    r.color('purple')
    r.dot(5)
    r.shapesize(-1.0,1.0)

    w = Turtle(shape=tsvg)
    w.up()
    w.goto(100,-200)
    w.down()
    w.color('orange')
    w.dot(5)
    w.shapesize(1.0,-1.0)



async def test_fumetti_piu():

    _info("TEST FUMETTI: BEGINNING...")
    t = Sprite()
    t.speed(10)
    carica_immagine(t, 'img/ch-archeologist-e.gif')
    
    await dire(t, "abcdefghilmnopqrstuvzABCDEFGHILMNOPQRSTUVZ",2)
    await dire(t, "Più in alto",2, dy = 120)
    await dire(t, "Più in basso",2, dy = -120)
    await dire(t, "Più a destra",2, dx = 120)
    await dire(t, "Più a sinistra",2, dx = -120)
    
    _info("TEST FUMETTI: DONE...")

async def test_fumetti_ciao():

    _info("TEST FUMETTI CIAO: BEGINNING...")
    t = Sprite()
    t.speed(10)
    carica_immagine(t, 'img/ch-archeologist-e.gif')
    
    await dire(t, "Ciao1", 1)
    t.goto(-250, 0)
    await dire(t, "Ciao2", 1)
    t.goto(250, 0)
    await dire(t, "Ciao3", 1)
    t.goto(0, 250)
    await dire(t, "Ciao4", 1)
    t.goto(0, -250)
    await dire(t, "Ciao5", 1)
    t.goto(250, -250)
    await dire(t, "Ciao6", 1)
    t.goto(-250, 250)
    await dire(t, "Ciao7", 1)
    t.goto(-250, -250)
    await dire(t, "Ciao8", 1)
    t.goto(250, 250)
    await dire(t, "Ciao9", 1)
    
    _info("TEST FUMETTI CIAO: DONE...")


def test_big_star():
    """from Python official examples (and without transcript done() calls)
    """
    up ()
    goto (-250, -21)
    startPos = pos ()

    down ()
    color ('red', 'yellow')
    begin_fill ()
    while True:
        forward (500)

        right (170)

        if distance (startPos) < 1:
            break
    end_fill ()


def test_text():
    
    color('black', 'white')
    dot(10)
    color('red')
    write("Writing align center", align="center")

    goto(-100,100)


    color('black', 'white')
    dot(10)
    color('green')    
    write("Writing align left", align="left")

    goto(100,-100)
    color('black', 'white')
    dot(10)
    color('blue')
    write("Writing align right", align="right")


def test_colors():
    pensize(5)
    up()
    goto(-200,-110)
    down()
    pencolor(255,0,0)
    forward(100)
    pencolor((0,255,0))
    forward(100)
    pencolor((0,0,255))
    forward(100)
    pencolor('purple')
    forward(100)
    print('pencolor:', pencolor())
    print('fillcolor:', fillcolor())

    pencolor('yellow')
    fillcolor(255,0,0)

    up()
    goto(-50,0)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()

    pencolor('cyan')
    fillcolor((0,255,0))

    up()
    goto(0,-50)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()

    pencolor('orange')
    fillcolor((0,0,255))

    up()
    goto(50,0)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()

    pencolor('grey')
    fillcolor('purple')

    up()
    goto(0,50)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()


async def test_quadrato_pieno():
    begin_fill()
    pencolor('red')
    fillcolor('green')
    print('pencolor:', pencolor())
    print('fillcolor:', fillcolor())

    begin_fill()
    for i in range(4):
        forward(100)
        await asyncio.sleep(0.5)
        left(90)
        await asyncio.sleep(0.5)
    end_fill()


async def test_storytelling():
    hideturtle()  # nasconde quella di default

    ada = Turtle()                                # crea una NUOVA tartaruga
    ada.hideturtle()
    ada.screen.bgpic("img/bg-seaside-2.gif") 

    carica_immagine(ada, "img/ch-archeologist-e.gif")  # nostro comando speciale
    ada.penup()                                   # su la penna!
    ada.goto(-100,0)                              # spostati sul lato sinistro
    ada.showturtle()                                

    bob = Turtle()
    bob.hideturtle()
    carica_immagine(bob, "img/ch-arctic-big-w.gif")
    bob.penup()
    bob.goto(100,0)
    bob.showturtle()

    await dire(ada, "Ciao! Io sono Ada!", 3)
    await dire(ada, "Tu come ti chiami?", 3)
    await dire(bob,"Io sono Bob!", 2)
    await dire(bob,"Mi sono perso!", 3)
    await dire(ada,"Si vede!", 2)
    await dire(ada,"Esploriamo la foresta?", 4)
    await dire(bob,"Ok!", 2)
    bob.goto(250, 0)
    ada.goto(250, 0)

    ada.screen.bgpic("img/bg-forest-1.gif")
    ada.speed(0)   # velocissima
    bob.speed(0)   # velocissimo
    bob.goto(-200, 0)
    ada.goto(-200, 0)
    ada.speed(5)   # normale
    bob.speed(5)   # normale
    ada.goto(-100, -0)
    bob.goto(100, -0)

    await dire(ada,"Qua fa più fresco!", 3)
    await dire(bob,"Per me è ancora troppo caldo!", 6)




