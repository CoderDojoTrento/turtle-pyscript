
import sys 
import html

from pyscript import document
from pyscript.js_modules import marked
from pyscript.js_modules import turtleps as tpsjs


    
if "pyodide" in sys.modules:
    SYSTEM = "pyodide"
elif sys.implementation.name == "micropython":
    SYSTEM = "micropython"
else:
    raise Exception("Unknown python platform!")




SVGNS = 'http://www.w3.org/2000/svg'

if SYSTEM == "micropython":
    cur_fname = lambda n=0: "Can't get current function name in micropython"
else:
    cur_fname = lambda n=0: sys._getframe(n + 1).f_code.co_name

def get_fun_doc(f):
    return f.__doc__ if SYSTEM != 'micropython' else "Can't parse function doc with micropython"


def add_classes(obj, cs):
    """cs: a string of space-separated classes"""
    curc = obj.getAttribute('class')
    if curc:
        obj.setAttribute('class', curc + ' ' + cs)
    else:
        obj.setAttribute('class', cs)

class VisualTest:
    def __init__(self, 
                 ititle, 
                 idescription, 
                 ivisual, 
                 itest_area=None, 
                 width=400, 
                 height=400,
                 css_class='',
                 title_level=1):

        maxw = width if type(width) is str else f"{max(400, width)}px"
        def setw(el):
            el.style.maxWidth = maxw; 
            el.style.maxHeight= f"{max(400, height)}px"

        if itest_area:
            self.test_area = itest_area  #container
        else:
            self.test_area = document.getElementById('tps-test-area')  #container

        self.script_doc = document.createElement('div')
            
        self.title = document.createElement(f'h{title_level}')
        self.description = document.createElement('div')
        
        self.title.innerHTML = ititle

        setw(self.title)
        add_classes(self.title, 'tps-script-title') 
            
        if idescription == None:
            pass            
        else:
            self.description.innerHTML = marked.parse(idescription)
        
        setw(self.description)
        add_classes(self.description, 'tps-script-description') 

        self.visual_wrapper = document.createElement('div')
        self.visual = ivisual
        
        
        setw(self.visual_wrapper)
        self.visual_wrapper.setAttribute('class', 'tps-test-visual-wrapper')
        
        self.visual_wrapper.appendChild(self.visual)

        self.test_box = document.createElement('div')
        
        self.test_box.setAttribute('class', 'tps-test-preview' + ' ' + css_class)

        self.test_box.appendChild(self.script_doc)
        self.script_doc.appendChild(self.title)
        self.script_doc.appendChild(self.description)
        self.test_box.appendChild(self.visual_wrapper)        
        
        self.test_area.appendChild(self.test_box)


class VisualTestSuite(VisualTest):


    # Made it like this to have minimum common denominator working in micropython:
    # Note in micropython:
    #    __name__: "__main__" can't be found in sys.modules
    #    __file__:   not defined
    #    os.getcwd(): "/"
    #    __init__: can't be async

    def __init__(self, title, desc, itest_area=None):
        """ Call it with:
            title , desc = await tpsjs.fetch_title_desc('test/uitests_all.py')  
        """        
        VisualTest(title,
                   desc,
                   document.createElement('div'),
                   width='100%',
                   itest_area=itest_area,
                   css_class='tps-test-suite')
