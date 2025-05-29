"""<a href="https://github.com/CoderDojoTrento/turtle-pyscript" target="_blank">Turtle Pyscript</a> tests, by <a href="https://www.coderdojotrento.it" target="_blank">CoderDojoTrento</a>
        
<h2>It may take sometime to load everything ...</h2>
"""
import sys 
import os
import ast
from pyodide.ffi import create_proxy
from pyscript import document, window, config, fetch
from tps_testing import *
from pyscript import config 


#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
#tps._tracing = False


class VisualFrameTest(VisualTest):
    def __init__(self, test_path, descr,v,v_code,*args):
        iframe = document.createElement('iframe')
        #test_name = os.path.split(test_path)[1][:-3]

        iframe.setAttribute('src', f"test.html?s={test_path}&navbar=false&sticky=true&show_desc=false&v={v}&v_code={v_code}" )
        iframe.setAttribute('width', 400 + 30)
        iframe.setAttribute('height', 400 + 100)
        iframe.style.overflowX = 'hidden'

        the_title, the_descr = tpsjs.sep_title_desc(test_path, descr)
        
        super().__init__(f'<a href="test.html?s={test_path}&v={v}&v_code={v_code}" target="_blank" >{the_title}</a>',
                         the_descr,  
                         iframe, 
                         width=420,
                         title_level=2,
                         *args)
        self.test_box.style.minHeight = "550px"
        self.test_box.style.overflowX = "hidden"
        self.visual_wrapper.style.minHeight = "520px"
        self.visual_wrapper.style.overflowX = 'hidden'

VisualTestSuite(sys.modules[__name__])


print('list', list(config['files']))

i = 0
for test_path in config['files']:
    print("Found test_path:", test_path)

    test_path = test_path.replace("{V}", config["files"]["{V}"])
    test_path = test_path.replace("{V_CODE}", config["files"]["{V_CODE}"])

    
    if test_path.startswith('test/uitest_'):
        data = await fetch(test_path).text()
        doc = ast.get_docstring(ast.parse(data))
        if not doc:
            doc = ''
        VisualFrameTest(test_path.split('?')[0], 
                        doc,
                        config["files"]["{V}"], 
                        config["files"]["{V_CODE}"])
        i += 1
        #if i == 2: break
        