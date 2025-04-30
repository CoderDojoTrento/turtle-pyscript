""" Tracing tests

Each row shows:
original svg -> original image canvas rendition -> traced svg silohuette 

"""

import sys 
import js
from pyscript.ffi import create_proxy
from pyscript import document, window
from tps_testing import *
from pyscript.js_modules import turtleps as tpsjs


    
def f(e, work_img, target):
    work_canvas = tpsjs.vectorize(work_img, target)
    
    target.setAttribute('width', work_img.width)
    target.setAttribute('height', work_img.height)
    target.setAttribute('class', 'tps-test-tracing-steps' )

    tracing_steps = document.createElement('div')
    tracing_steps.setAttribute('class', 'tps-test-tracing-steps' )

    work_img.setAttribute('class', 'tps-test-tracing-steps' )
    tracing_steps.appendChild(work_img)
    
    work_canvas.setAttribute('class', 'tps-test-tracing-steps' )
    tracing_steps.appendChild(work_canvas)
                    
    tracing_steps.appendChild(target)

    VisualTest(work_img.src[len(document.location.origin):], "", tracing_steps)

    #wsvg.appendChild(tracing_steps)

    js.console.log("Done placing children in target", target)


images =  ["img/ch-archeologist-e.gif",
           "img/turtle.svg",
           "img/an-dino-1e.gif",
           "img/ch-arctic-big-e.gif",
           "img/vh-rocket-1ut.gif",
           "img/warning.svg",
           "img/ob-energy.gif",
           "test/img/double-circle.svg",
           "test/img/donut.svg",
]



VisualTestSuite(sys.modules[__name__])

i = 0
for imm in images:

    work_img = js.Image.new()
    work_img.src = imm
    target = document.createElementNS(SVGNS, 'svg')

    def imm_loaded(work_img, target):
        js.console.log("Loaded image!", work_img,
                        "work_img.src:", work_img.src, 
                        "work_img.width:", work_img.width, 
                        "work_img.height:", work_img.height )
        return lambda e: f(e, work_img, target)

    work_img.onload = imm_loaded(work_img, target)

    i += 1
