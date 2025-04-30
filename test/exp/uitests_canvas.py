"""Canvas tests

<span>Some tests to check native canvas drawing shortcomings, in particular Chrome 135.0.7049.114  
doesn't want to draw <pre><image></pre> elements :-/
  
</span>
"""

from turtleps import *
import turtleps as tps
import math
import inspect 

from pyscript.js_modules import Canvg

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
tps._tracing = False

cur_fname = lambda n=0: sys._getframe(n + 2).f_code.co_name


import js
def GetImageAsXMLFromInline(svg_el):
    """ TODO WIP (note: at least encoding works for plain non-loaded svg) 
    """
    #xml = js.encodeURIComponent(svg_el.outerHTML);
    '''
    xml = js.encodeURIComponent("""
                                <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="400" height="400">
                                  
                                </svg>
                                
                                """
                                
                                )
    '''

    html = js.XMLSerializer.new().serializeToString(svg_el)

    html = '<image href="img/an-dino-1e.gif"><image>'

    encoded = js.encodeURIComponent(f'''
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <defs>
            <image href="{iicon}" id="prova"></image>
        </defs>

    {html}</svg>
                                    
    ''')
    #Chrome bug seems to prebent correct embedded <image> display  https https://bugs.webkit.org/show_bug.cgi?id=39059
    
    image_data = f'data:image/svg+xml;utf8,{encoded}' ;
    svg_img = js.Image.new();
    svg_img.src = image_data;

    return svg_img;



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



test_area = document.getElementById('test-area');

def create_wcanvas(width=400, height=400):
    canvas = document.createElement('canvas')


    canvas.setAttribute('style',f"border-width:1px; border-color:black; border-style:solid; max-width:{width}px; max-height:{height}px;")
    canvas.setAttribute('width', width)
    canvas.setAttribute('height', height)

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

async def make_test(s):
    size = Screen()._shapes[idino].get_svg_image_size()
    tps._info('size=', size)
    wcanvas = create_wcanvas()

    wcanvas._title.textContent = cur_fname()
      
    ctx = wcanvas._canvas.getContext("2d");
    

    encoded = js.encodeURIComponent(f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
                                             width="{int(size[0])}" 
                                             height="{int(size[1])}">
        {s}
    </svg> 
    ''')
    image_data = f'data:image/svg+xml;utf8,{encoded}' ;
    svg_img = js.Image.new();
    svg_img.src = image_data;


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

    tps._info('waiting...')

    def f(e):
        tps._info("Image loaded!")
        ctx.drawImage(svg_img, 0, 0);
        p = ctx.getImageData(px, py, 1, 1).data; 
        tps._info("central point after drawing", p, c=True)
        tps._info("central point alpha", p[3], c=True)
        
        
        u = ctx.getImageData(ux, uy, 1, 1).data; 
        tps._info("upper-left point after drawing", u, c=True)
        tps._info("central point alpha", u[3], c=True)
        

        draw_circle(wcanvas._canvas, px,py, 'green')
        draw_circle(wcanvas._canvas, ux,uy, 'red')

    svg_img.onload = f


async def test_replicate_canvas_box_verbatim_no_include_defs_no_transpose():
    await make_test(
        '<rect width="150" height="150" fill="rgb(0, 255, 0)" stroke-width="1" stroke="rgb(0, 0, 0)" />'
    )

async def test_replicate_canvas_gif_image_verbatim_no_include_defs_no_transpose():
    await make_test('<image href="img/an-dino-1e.gif"></image>')
    

async def test_replicate_canvas_gif_verbatim_no_include_defs_no_transpose():
    await make_test('''
    <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use>
''')
    
    

async def test_replicate_canvas_gif_verbatim_include_defs_no_transpose():    
    await make_test('''
        <defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" ></use> 
    ''')

async def test_replicate_canvg_gif_verbatim_include_defs_with_transpose():
    await make_test('''
        <defs>
            <image href="img/an-dino-1e.gif" id="img-an-dino-1e-gif"></image>
        </defs>
        <g id="sprite-15156160" transform="translate(300,200)" style="background-color: black;">
            <use href="#img-an-dino-1e-gif" fill="black" stroke="black" stroke-width="1" fill-rule="evenodd" 
            transform="translate(-138.0, -118.0) rotate(0.0) scale(0.7,0.7)" 
            transform-origin="138.0 118.0">
            </use>
        </g>
    ''')



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


await test_replicate_canvas_box_verbatim_no_include_defs_no_transpose()

await test_replicate_canvas_gif_image_verbatim_no_include_defs_no_transpose()

await test_replicate_canvas_gif_verbatim_no_include_defs_no_transpose()


await test_replicate_canvas_gif_verbatim_include_defs_no_transpose()

#await test_replicate_canvg_gif_verbatim_include_defs_with_transpose()

