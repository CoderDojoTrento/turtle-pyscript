
import sys 
import html

from pyscript import document
from pyscript.js_modules import marked
from pyscript.js_modules import turtleps as tpsjs


SVGNS = 'http://www.w3.org/2000/svg'

cur_fname = lambda n=0: sys._getframe(n + 1).f_code.co_name

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
    def __init__(self, module, itest_area=None):
        """ Call it with sys.modules[__name__] """        

        self.module = module
        title, descr = tpsjs.sep_title_desc('', self.module.__doc__)
        VisualTest(title,
                   descr,
                   document.createElement('div'),
                   width='100%',
                   itest_area=itest_area,
                   css_class='tps-test-suite')
