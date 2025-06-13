
"""Canvg 4.0.3 tests

<span>Some tests to check <a href="https://github.com/canvg/canvg">canvg</a> library which we don't actually use, I put them here for reference 
</span>
"""


from turtleps import *
import turtleps as tps
from tps_testing import *
import math
import inspect 

from pyscript.js_modules import Canvg

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False


def draw_circle(canvas, x, y, color):
    ctx = canvas.getContext('2d');
    radius = 10;

    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * math.pi, False);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = 5;
    ctx.strokeStyle = '#003300';
    ctx.stroke();    



test_area = document.getElementById('tps-test-area');

def create_wcanvas(width=None, height=None):
    canvas = document.createElement('canvas')
    
    canvas.setAttribute('style',"border-width:1px; border-color:black; border-style:solid;")

    wcanvas = document.createElement('div')
    title = document.createElement('a')
    wcanvas.setAttribute('class', 'tps-test-preview')

    #title.setAttribute('style', "font-weight:")
    wcanvas.appendChild(title)
    wcanvas.appendChild(canvas)
    test_area.appendChild(wcanvas)
    
    wcanvas._canvas = canvas
    wcanvas._title = title
    return wcanvas

async def make_test(t, width=None, height=None):

    if width:
        the_width = width
    else:
        the_width = 400

    if height:
        the_height = height
    else:
        the_height = 400
    
    
    wcanvas = create_wcanvas(width, height)
    
    wcanvas._title.textContent = cur_fname(1)
      
    ctx = wcanvas._canvas.getContext("2d");
    
    cvg = Canvg.Canvg

    #s = f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{the_width}" height="{the_height}">
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" >
     
        {t}
    </svg> 
    '''
    px = 138
    py = 118
    p = ctx.getImageData(px, py, 1, 1).data; 
    tps._info("central point before drawing", p, c=True)
    tps._info("central point alpha", p[3], c=True)

    ux = 10
    uy = 10

    u = ctx.getImageData(ux, uy, 1, 1).data; 
    tps._info("upper-left point before drawing", u, c=True)
    tps._info("upper point alpha", u[3], c=True)


    v = cvg.fromString(ctx, s) 

    tps._info('v=', v, c=True)
    tps._info('waiting...')
    await asyncio.sleep(1)
    tps._info("v run")
    v.render();
    p = ctx.getImageData(px, py, 1, 1).data; 
    tps._info("central point after drawing", p, c=True)
    tps._info("central point alpha", p[3], c=True)
    
    
    u = ctx.getImageData(ux, uy, 1, 1).data; 
    tps._info("upper-left point after drawing", u, c=True)
    tps._info("central point alpha", u[3], c=True)
    

    draw_circle(wcanvas._canvas, px,py, 'green')
    draw_circle(wcanvas._canvas, ux,uy, 'red')



async def test_replicate_canvg_gif_verbatim_no_include_defs_no_transpose():
    """
    doesn't work
    """    
    
    await make_test(f'''
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>
    ''')
    

async def test_replicate_canvg_gif_verbatim_include_defs_no_transpose():
    """
    works
    """    
    await make_test('''<defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>)
    ''')

async def test_replicate_canvg_gif_verbatim_include_defs_with_transpose():
    """
    somehow transpose is not correct..
    """    
    
    await make_test(f'''
        <defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <g id="sprite-15156160" transform="translate(300,200)" style="background-color: black;">
            <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" 
            transform="translate(-138.0, -118.0) rotate(0.0) scale(0.7,0.7)" 
            transform-origin="138.0 118.0">
            </use>
        </g>
    ''', width=400, height=400)

async def test_replicate_canvg_all():
    await make_test(Screen().svg.outerHTML)

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

title , desc = await tpsjs.fetch_title_desc('test/uitests_canvg.py')
VisualTestSuite(title, desc)


await test_replicate_canvg_gif_verbatim_no_include_defs_no_transpose()


await test_replicate_canvg_gif_verbatim_include_defs_no_transpose()

await test_replicate_canvg_gif_verbatim_include_defs_with_transpose()

await test_replicate_canvg_all()

