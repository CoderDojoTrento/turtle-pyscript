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
    
    ada = Sprite()

    ada.screen.register_shape('img/turtle.svg')
    ada.shape('img/turtle.svg')

    #await asyncio.sleep(1)

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
    
    _info("TEST TURTLEPS: DONE...")

async def test_tilt():
    screen = Screen()
    screen.register_shape('img/turtle.svg')

    ada = Turtle()
    bob = Turtle()


    ada.shape('img/turtle.svg')
    heading_before = ada.heading()

    await asyncio.sleep(0.5)
    ada.tilt(40)
    assert heading_before == ada.heading()

    for i in range(4):
        await asyncio.sleep(0.5)
        ada.forward(100)
        await asyncio.sleep(0.5)
        ada.left(90)


    await asyncio.sleep(0.5)
    bob.tilt(-40)
    bob.setheading(-90)
    assert heading_before == ada.heading()

    await asyncio.sleep(0.5)
    bob.forward(100)
    await asyncio.sleep(0.5)
    bob.left(90)
    await asyncio.sleep(0.5)
    bob.forward(100)



async def test_shapesize_one():
    arc = 'img/ch-archeologist-e.gif'
    screen = Screen()
    screen.register_shape(arc)
    #hideturtle()
    shape(arc)
    color('green')
    dot(5)
    shapesize(3.0)
    

async def test_shapesize_many():
    arc = 'img/ch-archeologist-e.gif'
    tsvg = 'img/turtle.svg'
    screen = Screen()
    screen.register_shape(arc)
    screen.register_shape(tsvg)
    
    # TODO make proper wait https://github.com/CoderDojoTrento/turtle-pyscript/issues/8
    await asyncio.sleep(0.3)

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
    p.goto(-100,150)
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
    r.goto(-100,-150)
    r.down()
    r.color('purple')
    r.dot(5)
    r.shapesize(1.0,-1.0)

    w = Turtle(shape=tsvg)
    w.up()
    w.goto(100,-150)
    w.down()
    w.color('orange')
    w.dot(5)
    w.shapesize(-1.0,-1.0)



async def test_fumetti_piu():

    _info("TEST FUMETTI: BEGINNING...")
    t = Sprite()
    t.speed(10)
    t.load_image('img/ch-archeologist-e.gif')
    
    await t.say("abcdefghilmnopqrstuvzABCDEFGHILMNOPQRSTUVZ",2)
    await t.say("Più in alto",2, dy = 120)
    await t.say("Più in basso",2, dy = -120)
    await t.say("Più a destra",2, dx = 120)
    await t.say("Più a sinistra",2, dx = -120)
    
    _info("TEST FUMETTI: DONE...")

async def test_fumetti_ciao():

    _info("TEST FUMETTI CIAO: BEGINNING...")
    t = Sprite()
    t.speed(10)
    t.load_image('img/ch-archeologist-e.gif')
    
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

    screen = Screen()
    screen.bgpic("img/bg-seaside-2.gif") 
    screen.register_shape("img/ch-archeologist-e.gif")
    screen.register_shape("img/ch-arctic-big-e.gif")

    await asyncio.sleep(0.5)  # to allow loading of images

    ada = Sprite()                                # Sprite instead of Turtle
    ada.hideturtle()
    
    ada.load_image("img/ch-archeologist-e.gif")   # looks east
    ada.penup()  
    ada.goto(-100,0)                              # move to left side 
    ada.showturtle()                                

    bob = Sprite()
    bob.hideturtle()
    bob.load_image("img/ch-arctic-big-e.gif")   # looks east
    bob.shapesize(-1.0,1.0)   # looks left keeping head on top
    bob.penup()
    bob.goto(100,0)
    bob.showturtle()

    
    await ada.say("Ciao! Io sono Ada!", 3)
    await ada.say("Tu come ti chiami?", 3)
    await bob.say("Io sono Bob!", 2)
    await bob.say("Mi sono perso!", 3)
    await ada.say("Si vede!", 2)
    await ada.say("Esploriamo la foresta?", 4)
    await bob.say("Ok!", 2)
    bob.shapesize(1.0,1.0)    # looks right
    
    for i in range(28):
        bob.goto(bob.xcor()+5, bob.ycor())
        await asyncio.sleep(0.05)

    for i in range(65):
        ada.goto(ada.xcor()+5, ada.ycor())
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
        bob.goto(bob.xcor()+5, bob.ycor())
        await asyncio.sleep(0.05)

    bob.shapesize(-1.0, 1.0)  # looks left
    
    for i in range(27):
        ada.goto(ada.xcor()+5, ada.ycor())
        await asyncio.sleep(0.02)

    #ada.goto(-100, -0)   # currently immediate
    #bob.goto(100, -0)    # currently immediate

    await ada.say("Qua fa più fresco!", 3)
    await bob.say("Per me è ancora troppo caldo!", 6)
    

def test_load_image():
    ada = Sprite()
    ada.load_image("img/ch-archeologist-e.gif")
    ada = Sprite()
    ada.load_image("img/ch-archeologist-e.gif")

def test_stamp():

    for i in range(5):
        goto(i*50-150,0)
        stamp()
    
    ada = Sprite()
    ada.load_image("img/ch-archeologist-e.gif")
    ada.goto(-100,-100)
    for i in range(5):
        goto(i*50-150,0)
        ada.stamp()


async def test_layers():
    ada = Sprite()
    ada.load_image("img/ch-archeologist-e.gif")

    bob = Sprite()
    bob.load_image("img/ch-arctic-big-w.gif")

    await asyncio.sleep(1)
    
    ada.to_foreground()

    await asyncio.sleep(1)

    ada.to_background()


def test_lag():
    
    for i in range(500):
        forward(100)
        left(90)
        color('red')  # should create a new path

async def test_interactive_loop():

    screen = Screen()
    screen.bgpic("img/bg-space-1.gif") 
    screen.register_shape("img/bg-space-1.gif")
    screen.register_shape("img/vh-rocket-1ut.gif")

    await asyncio.sleep(0.3)  # TODO improve when we have proper awaiting register_shape

    rocket = Sprite()
    rocket.shape("img/vh-rocket-1ut.gif")  # rocket looks up
    rocket.pensize(5)
    rocket.pendown()
    rocket.tilt(-90)   # fix image orientation - NOTE: original Python turtle doesn't allow this for images, only for polygons!
    
    # outside main loop we can use await stuff for intro animations

    await rocket.say("Are you ready?", 2)  
    await rocket.say("Use arrow keys!", 2)  
    

    init_engine()

    def update():
        # workaround for lag:  https://github.com/CoderDojoTrento/turtle-pyscript/issues/18 
        # if you keep setting color, it creates a new svg path element, which is faster than 
        # enlarging the current path string
        rocket.color('yellow') 

        if pressed("ArrowUp"):
            print("ArrowUp")
            rocket.forward(5)

        if pressed("ArrowLeft"):
            print("ArrowLeft")
            rocket.left(6)

        if pressed("ArrowRight"):
            print("ArrowRight")
            rocket.right(6)

        set_timeout(update, interval)    


    update()


"""
#stop_button = pydom[".cdtn-stop-button"]

#@pydom.when(stop_button, 'click')
#def hi():
#    alert("hi")

def text(x, y, text: str, color):
    ctx.font = "11px Monospace"
    ctx.textAlign = 'left'
    if(color == 7):
        ctx.fillStyle = '#fff'

    ctx.fillText(text, x*_scale, y*_scale)

def centered_text(text: str, color):
    if color == 7:
        ctx.fillStyle = '#fff'

    ctx.textAlign = 'center'
    ctx.fillText(text, (canvas_width*_scale) / 2, (canvas_height*_scale) / 2)

"""
# CAN'T DO WHEN ALREADY IN AN EVENT LOOP
"""
asyncio.run(asyncio.gather(
    
    test_turtleps(),
    test_fumetti(),
))
"""

# this works!
"""
asyncio.gather(
    
    test_turtleps(),
    test_fumetti(),
)

print("Fine main.py")
"""

"""
def check_type(arg, *types):
    for t in types:
        if type(arg) == t:
            return
    raise CDTNException(f"Tipo di dato sbagliato per il valore {arg    }!\n Atteso: {types} Ottenuto: {type(arg)}")


"""