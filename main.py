import random
#import pyscript.web.dom
from pyscript import when, display
from pyscript.web import page, img

from js import DOMParser
from js import (
    document,
    Element,
)


from pyscript import window, document

from pyodide.http import open_url
from pyodide.ffi.wrappers import set_timeout
from pyodide.ffi.wrappers import add_event_listener


from turtleps import *
#from cdtnge import *

ctx = None
interval=200  # TODO

_pressedKeys = {
}

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


def _handle_input(e):
    """ {
     "key": "a",
     "keyCode": 65,
     "which": 65,
     "code": "KeyA",
     "location": 0,
     "altKey": false,
     "ctrlKey": false,
     "metaKey": false,
     "shiftKey": false,
     "repeat": false
    }

    {
     "key": "ArrowLeft",
     "keyCode": 37,
     "which": 37,
     "code": "ArrowLeft",
     "location": 0,
     "altKey": false,
     "ctrlKey": false,
     "metaKey": false,
     "shiftKey": false,
     "repeat": false
    }
    """
    global _pressedKeys
    if e.type == "keydown":
        _pressedKeys[e.key] = True
    elif e.type == "keyup":
        _pressedKeys[e.key] = False

def btn(key: str):
    if key in _pressedKeys:
        return _pressedKeys[key]
    else:
        return False

#stop_button = pydom[".cdtn-stop-button"]

#@pydom.when(stop_button, 'click')
#def hi():
#    alert("hi")


def init(sprite, append=True):
    global ctx 

    sprite.url = "./antigravity.svg"
    sprite.target = page["body"][0]

    doc = DOMParser.new().parseFromString(
        open_url(sprite.url).read(), "image/svg+xml"    
    )

    #doc = img(src=sprite.url)
    #page.append(open_url(sprite.url).read())
    
    sprite.node = doc.documentElement

    #sprite.node = doc._dom_element

    
    
    ctx = sprite.node

    if append:
        sprite.target.append(sprite.node)
    else:
        sprite.target._js.replaceChildren(sprite.node)

    sprite.x, sprite.y = 0, 0

     #init input
    add_event_listener(
        document,
        "keydown",
        _handle_input
    )

    add_event_listener(
        document,
        "keyup",
        _handle_input
    )

        

def update():
    global ctx, sprite
    
    if btn("ArrowUp") or btn(" "):
        print("DAVID: KEY_UP or KEY_SPACE")
        
    if btn("q"):
        print("DAVID: KEY_Q")
        print("DAVID: QUITTING!")
        return

    char = sprite.node.getElementsByTagName("g")[1]
    
    char.setAttribute("transform", f"translate({sprite.x}, {-sprite.y})")
    sprite.x += random.normalvariate(0, 1) / 20
    if sprite.y < 50:
        sprite.y += 0.1
        sprite.x -= 0.1
    else:
        sprite.y += random.normalvariate(0, 1) / 20
        
    set_timeout(update, interval)    

    

def check_type(arg, *types):
    for t in types:
        if type(arg) == t:
            return
    raise CDTNException(f"Tipo di dato sbagliato per il valore {arg    }!\n Atteso: {types} Ottenuto: {type(arg)}")


        




#sprite = ada
#init(ada, append=True)
#rettangolo = ada.add_rect(30,40,fill='rgb(0,255,255)', sid='pippo')
#rettangolo.setAttribute("fill", "green")
#rettangolo.fill = "green"  # non funziona
#update()


screen = Screen()
screen.register_shape('img/turtle.svg')


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
done ()

#import time
import asyncio

# one after the other
"""
await test_turtleps()
await test_fumetti()
"""

# CAN'T DO WHEN ALREADY IN AN EVENT LOOP
"""
asyncio.run(asyncio.gather(
    
    test_turtleps(),
    test_fumetti(),
))
"""

# this works!
asyncio.gather(
    
    test_turtleps(),
    test_fumetti(),
)
print("Io vengo eseguito IMMEDIATAMENTE DOPO!")

