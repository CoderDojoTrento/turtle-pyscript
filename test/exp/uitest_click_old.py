
from turtleps import *
import turtleps as tps
import inspect 

from pyscript.js_modules import Canvg

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

cur_fname = lambda n=0: sys._getframe(n + 1).f_code.co_name

screen = Screen()

idino = "img/an-dino-1e.gif"
iturtle = "img/turtle.svg"

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

def click_screen(event):
    """ This should be called before all others
    """
    tps._info("Clicked screen, event:", event,  c=True)
    
    event.stopPropagation()
    return False

tps._svg.onclick = click_screen

import js
def GetImageAsXMLFromInline(svg_el):

    #xml = js.encodeURIComponent(svg_el.outerHTML);
    '''
    xml = js.encodeURIComponent("""
                                <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                                  
                                </svg>
                                
                                """
                                
                                )
    '''

    #xml = js.encodeURIComponent(f'')
    html = svg_el.outerHTML
    html = js.XMLSerializer.new().serializeToString(svg_el)
    #html = '<rect width="150" height="150" fill="rgb(255, 0, 0)" stroke-width="1" stroke="rgb(0, 0, 0)" />'

    #encoded = js.encodeURIComponent(f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1"><defs><image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image></defs>{html}</svg>')
    html = '<use href="#prova"></use>'
    #html = '<image xlink:href="img/an-dino-1e.gif"><image>'
    iicon = '<image href="data:image/png;svgedit_url=http%3A%2F%2Ffabicon.ru%2Ftech%2Fsvg-edit%2Fimages%2Fitalic.png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAfklEQVRIie2UQQ3AMAwDj0IplEIpjMIojEIpDMuwlEIpjEL3aKR1fcePST3JX1txosBiMXEADahAUgRUC2hAVgTIJ/g32VRNrrRJkgWXIUCy4NvMi8J8R1zPhbCeMJhL6smI6xn/T6S/i+hlnvje/0lfuBuB9/4LsHmaLwB4ACwSKvguQ4XUAAAAAElFTkSuQmCC"></image>'
    
    #html = '<image xlink:href="test/img/square.svg"><image>'
    #html = '<image href="test/img/square.svg"><image>'

    encoded = js.encodeURIComponent(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><defs><image xlink:href="{iicon}" id="prova"></image></defs>{html}</svg>')
    #Chrome bug seems to prebent correct embedded <image> display  https https://bugs.webkit.org/show_bug.cgi?id=39059
    
    image_data = f'data:image/svg+xml;utf8,{encoded}' ;

    svg_img = js.Image.new();

    # "http://upload.wikimedia.org/wikipedia/commons/d/d2/Svg_example_square.svg" 
    svg_img.src = image_data;

    return svg_img;


async def test_replicate_canvg_gif_include_defs_no_transl():
    """
    works
    """    


    canvas = document.createElement('canvas')

    canvas.setAttribute('width', 400)
    canvas.setAttribute('height', 400)
    canvas.setAttribute('style',"border-width:1px; border-color:black; border-style:solid;")

    canvases = document.getElementById('canvases');

    wcanvas = document.createElement('div')
    title = document.createElement('div')
    title.textContent = cur_fname()
    title.setAttribute('style', "font-weight:")
    wcanvas.appendChild(title)
    wcanvas.appendChild(canvas)
    canvases.appendChild(wcanvas)
    
    ctx = canvas.getContext("2d");
    
    cvg = Canvg.Canvg

    s = f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>
    </svg> 
    '''

    v = cvg.fromString(ctx, s) 

    tps._info('v=', v, c=True)
    tps._info('waiting...')
    await asyncio.sleep(1)
    tps._info("v start")
    v.start();

    #p = ctx.getImageData(x, y, 1, 1).data
    #tps._info("point after drawing", p, c=True)

    #var hex = "#" + ("000000" + rgbToHex(p[0], p[1], p[2])).slice(-6);
    return True  # TODO



async def  detect_click(x,y, svg_el, svg_cont):
    
    canvas = document.getElementById('my-canvas')

    #canvas = document.createElement('canvas')

    #canvas.setAttribute('width', svg_cont.getAttribute("width"))<a
    #canvas.setAttribute('height', svg_cont.getAttribute('height'))

    canvas.setAttribute('width', 400)
    canvas.setAttribute('height', 400)

    
    #canvas = document.cre("canvas");
    ctx = canvas.getContext("2d");
    
    p = ctx.getImageData(x, y, 1, 1).data; 
    tps._info("point before drawing", p, c=True)
    
    #svg_img = GetImageAsXMLFromInline(svg_el)
    def f(e):
        tps._info("Image loaded!")
        ctx.drawImage(svg_img, 0, 0);


    svg_img.onload = f
    

    #const canvas = document.querySelector('canvas');
    #const ctx = canvas.getContext('2d');

    cvg = Canvg.Canvg

    iicon = '<image href="data:image/png;svgedit_url=http%3A%2F%2Ffabicon.ru%2Ftech%2Fsvg-edit%2Fimages%2Fitalic.png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAfklEQVRIie2UQQ3AMAwDj0IplEIpjMIojEIpDMuwlEIpjEL3aKR1fcePST3JX1txosBiMXEADahAUgRUC2hAVgTIJ/g32VRNrrRJkgWXIUCy4NvMi8J8R1zPhbCeMJhL6smI6xn/T6S/i+hlnvje/0lfuBuB9/4LsHmaLwB4ACwSKvguQ4XUAAAAAElFTkSuQmCC"></image>'
    #html = iicon
    #html = '<use href="#prova"></use>'
    
    #html = '<image xlink:href="test/img/square.svg"></image>'

    # works
    s = f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1">{iicon}</svg>' 

    # works
    html = '<image href="test/img/square.svg"></image>'
    s = f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1">{html}</svg>' 

    # works
    html = '<image href="img/an-dino-1e.gif"></image>'
    s = f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1">{html}</svg>' 

    # doesn't work
    html = '<image href="img/an-dino-1e.gif"></image>'
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>
    </svg> 
    '''

    # works
    html = '<image href="img/an-dino-1e.gif"></image>'
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>
    </svg> 
    '''

    v = cvg.fromString(ctx, s)  #'./svgs/1.svg');

    tps._info('v=', v, c=True)
    tps._info('waiting...')
    await asyncio.sleep(1)
    tps._info("v start")
    v.start();

    #tps._info("svg_img:", svg_img, c=True)

    #ctx.drawImage(svg_img, 0,0 )

    p = ctx.getImageData(x, y, 1, 1).data
    tps._info("point after drawing", p, c=True)

    #var hex = "#" + ("000000" + rgbToHex(p[0], p[1], p[2])).slice(-6);
    return True  # TODO

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

