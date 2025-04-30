""" Click tests

<span>See <a href="https://github.com/CoderDojoTrento/turtle-pyscript/issues/22" target="_blank"> issue 22 </a></span>

"""
import inspect
import sys 
from pyscript import document
from tps_testing import *

import js
from pyscript.js_modules import turtleps as tpsjs



N = 0   # test number

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
#tps._tracing = False


#screen = Screen()

idino = "img/an-dino-1e.gif"
iturtle = "img/turtle.svg"

'''
def click_screen(event):
    """ This should be called before all others
    """
    tps._info("Clicked screen, event:", event,  c=True)
    
    event.stopPropagation()
    return False

tps._svg.onclick = click_screen
'''


async def click(event):
    js.console.log("Clicked!, event:", event,  c=True)
    js.console.log("event.target: ", event.target) 

    d = await detect_click(event.x, event.y, event.target, None) # TODO should be container svg
    if d:
        js.console.log("detect_clicked!, event:", event,  c=True)


class VisualClickTest(VisualTest):
    def __init__(self, f, width=400, height=400,*args):
        svg = document.createElementNS(SVGNS, 'svg')
        svg.setAttribute('version', '1.1')
        svg.setAttribute('width', width)
        svg.setAttribute('height', height)
        svg.innerHTML = f()
        super().__init__(f.__name__, f.__doc__,  svg, *args)
        svg_el = document.getElementById(f'el{N}')
        svg_el.onclick = click



def test_image_gif():
    """
    Shows clicks (at least in Chrome) are (sadly) received by the whole bbox of the <image>
    Seems like PointerEvents are ignored
    """
    
    return f'''<image href="img/an-dino-1e.gif" id="el{N}"></image> '''


def test_image_gif_mask():

    return f'''
        <defs>
            <mask id="myMask{N}">   
                <rect x="0" y="0" width="150" height="150" fill="white"></rect>
            </masTestsk>
        </defs> 
        <image href="img/an-dino-1e.gif" id="el{N}" mask="url(#myMask{N})"></image>
    '''
    
def test_image_gif_clipped_clippath_in_defs():
    return f'''
        <defs>
            <clipPath id="clip{N}" clip-rule="evenodd">
                <rect x="130" y="115" width="50" height="25" fill="blue" ></rect>
            </clipPath>
        </defs> 
        <image href="img/an-dino-1e.gif" id="el{N}" clip-path="url(#clip{N})"></image>
    '''

def test_image_gif_clipped_complete():

    return f'''
        <defs>
            <g id="clip-paths{N}">
                <clipPath id="clip{N}" clip-rule="evenodd">
                    <rect x="130" y="115" width="50" height="25" fill="blue" ></rect>
                </clipPath>
            </g>
            <image href="img/an-dino-1e.gif" id="imgdef{N}" clip-path="url(#clip{N})"></image>

        </defs> 
        <g id="sprite-{N}" transform="translate(300,200)" style="background-color: black;">
            <use id="el{N}" href="#imgdef{N}" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" 
            transform="translate(-138.0, -118.0) rotate(45) scale(2,2)" 
            transform-origin="138.0 118.0">
            </use>
        </g>

    '''

def test_image_gif_pattern_t():
    """
    TODO Thought it might be useful, but it isn't
    https://stackoverflow.com/a/25230680    
    """

    return f'''
        <defs>
            <pattern id="pattern{N}" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
                <image href="img/turtle.svg" id="imgdef{N}"></image>
            </pattern>
        </defs> 

        <g id="sprite-{N}" transform="translate(0,20)" style="background-color: black;">
            <use id="el{N}" href="#imgdef{N}" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" 
            transform="translate(-138.0, -118.0) rotate(45) scale(2,2)" 
            transform-origin="138.0 118.0">
            </use>
        </g>
      
    '''


def test_image_gif_pattern_d():
    """
    TODO Thought it might be useful, but it isn't
    https://stackoverflow.com/a/25230680    
    """

    return f'''
        <defs>
            <pattern id="pattern{N}" x="0" y="0" width="277" height="237" patternUnits="userSpaceOnUse">
                <image href="img/an-dino-1e.gif" id="imgdef{N}"></image>
            </pattern>
        </defs> 

        <g id="sprite-{N}" transform="translate(300,200)" style="background-color: black;">
            <use id="el{N}" href="#imgdef{N}" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" 
            transform="translate(-138.0, -118.0) rotate(45) scale(0.3,0.3)" 
            transform-origin="138.0 118.0">
            </use>
        </g>

    '''


def test_vectorialize_image_svg():
    

    global N 
    N += 1

    #image_url = "img/ch-archeologist-e.gif"
    #image_url = "img/turtle.svg"
    image_url = idino

    width = 400
    height = 400

    f = test_vectorialize_image_svg

    s = f'''
        <defs>
            <clipPath id="clip{N}" clip-rule="evenodd">
            </clipPath>
            <image href="{image_url}" id="imgdef{N}" clip-path="url(#clip{N})"></image>
        </defs> 

        <g id="sprite-{N}" transform="translate(300,200)" style="background-color: black;">
            <use id="el{N}" href="#imgdef{N}" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" 
            transform="translate(-138.0, -118.0) rotate(45) scale(2,2)" 
            transform-origin="138.0 118.0">
            </use>
        </g>

    '''

    svg = document.createElementNS(SVGNS, 'svg')
    svg.setAttribute('version', '1.1')
    svg.setAttribute('width', width)
    svg.setAttribute('height', height)
    svg.innerHTML = s
    VisualTest(f.__name__, f.__doc__,  svg)
    svg_el = document.getElementById(f'el{N}')
    svg_el.onclick = click

    target = document.getElementById(f"clip{N}")

    def h(e, work_img, target):
        work_canvas = tpsjs.vectorize(work_img, target)        
        
    def imm_loaded(work_img, target):
        js.console.log("Loaded image!", work_img,
                        "work_img.src:", work_img.src, 
                        "work_img.width:", work_img.width, 
                        "work_img.height:", work_img.height )
        
        return lambda e: h(e, work_img, target)


    work_img = js.Image.new()
    work_img.src = image_url
    work_img.onload = imm_loaded(work_img, target)



async def test_use_image_gif():

    s = f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>
    </svg> 
    '''




async def  detect_click(x,y, svg_el, svg_cont):
    return False  # TODO




"""
screen.register_shape(idino)
screen.register_shape(iturtle)

await ge_init()


ada = Sprite()
ada.shape(iturtle)
ada.shapesize(0.7,0.7)
ada.goto(-100,0)

dino = Sprite()
dino.shape(idino)
dino.shapesize(0.7,0.7)
dino.goto(100,0)

async def click_ada(event):
    tps._info("Clicked ada, event:", event,  c=True)

    d = await detect_click(event.x, event.y, ada.svg, Screen().svg)
    if d:
        await ada.say("You clicked me!",2)

    #event.stopPropagation()

ada.svg.onclick = click_ada


async def click_dino(event):
    d = await detect_click(event.x, event.y, dino.svg, Screen().svg)
    if d:
        tps._info("Clicked dino, event:", event,  c=True)
    await dino.say("BAARK!",2)
    await dino.say("GUARK!", 2)

dino.svg.onclick = click_dino


"""

VisualTestSuite(sys.modules[__name__])



image_gif_tests = [f for name, f 
                     in inspect.getmembers(sys.modules[__name__], inspect.isfunction)
                     if name.startswith('test_image')]

for t in image_gif_tests:
    N += 1
    print("Processing:", t.__name__)
    VisualClickTest(t)


test_vectorialize_image_svg()