from turtleps import *

screen = Screen()
screen.bgpic("img/bg-space-1.gif") 
screen.register_shape("img/bg-space-1.gif")
screen.register_shape("img/vh-rocket-1ut.gif")

await ge_loaded()

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
