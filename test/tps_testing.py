
import sys 
import html

from pyscript import document
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
                 css_class=''):

        maxw = width if type(width) is str else f"{max(400, width)}px"
        def setw(el):
            el.style.maxWidth = maxw; 
            el.style.maxHeight= f"{max(400, height)}px"

        if itest_area:
            self.test_area = itest_area  #container
        else:
            self.test_area = document.getElementById('tps-test-area')  #container
        
        self.title = document.createElement('a')
        self.description = document.createElement('div')
        
        if ititle.strip().startswith('<'):
            self.title.innerHTML = ititle
        else:
            self.title.innerHTML = html.escape(ititle)
        
        setw(self.title)
        add_classes(self.title, 'tps-test-title')

        if idescription == None:
            pass            
        elif idescription.strip().startswith('<'):
            self.description.innerHTML = idescription
        else:
            self.description.innerHTML = html.escape(idescription)

        setw(self.description)
        add_classes(self.description, 'tps-test-description') 

        self.visual_wrapper = document.createElement('div')
        #if ivisual == None:
        #    self.visual = document.createElement('div')
        self.visual = ivisual
        #else:
        
        setw(self.visual_wrapper)
        self.visual_wrapper.setAttribute('class', 'tps-test-visual-wrapper')
        
        self.visual_wrapper.appendChild(self.visual)

        self.test_box = document.createElement('div')
        
        self.test_box.setAttribute('class', 'tps-test-preview' + ' ' + css_class)

        #title.setAttribute('style', "font-weight:")
        self.test_box.appendChild(self.title)
        self.test_box.appendChild(self.description)
        self.test_box.appendChild(self.visual_wrapper)        
        
        self.test_area.appendChild(self.test_box)


class VisualTestSuite(VisualTest):
    def __init__(self, module,itest_area=None):
        """ Call it with sys.modules[__name__] """        

        self.module = module
        splits = self.module.__doc__.split('\n')
        VisualTest(splits[0],
                    #self.module.__name__  'would show 'main.py'.... 
                   '\n'.join(splits[2:]),
                   document.createElement('div'),
                   width='100%',
                   itest_area=itest_area,
                   css_class='tps-test-suite')
