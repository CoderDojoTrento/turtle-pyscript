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
import asyncio


from turtleps import *



ctx = None
interval=20  # TODO  millisecs

_pressedKeys = {
}


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
        print("KEY_UP or KEY_SPACE")
        
    if btn("q"):
        print("KEY_Q")
        print("QUITTING!")
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

    

from tests import *

#sprite = ada
#init(ada, append=True)
#rettangolo = ada.add_rect(30,40,fill='rgb(0,255,255)', sid='pippo')
#rettangolo.setAttribute("fill", "green")
#rettangolo.fill = "green"  # non funziona
#update()

#hideturtle()

#await test_turtleps()


#test_stamp()

#test_big_star()

#await test_storytelling()

#test_load_image()

#await test_layers()

#await test_shapesize_one()

#await test_shapesize_many()

#await test_tilt()

#await test_quadrato_pieno()

#await test_fumetti_ciao()

#await test_fumetti_piu()

#test_text()
#test_colors()




