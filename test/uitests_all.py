"""<h1><a href="https://github.com/CoderDojoTrento/turtle-pyscript" target="_blank">Turtle Pyscript</a> tests, by <a href="https://www.coderdojotrento.it" target="_blank">CoderDojoTrento</a></h1>
        
<h2>It may take sometime to load everything ...</h2>
"""
import sys 
import os
import ast
from pyodide.ffi import create_proxy
from pyscript import document, window, config, fetch
from tps_testing import *

def gen_iframe(prj_name):
    return f'''
    <div class="tps-test-preview">
        <a href="{prj_name}.html" target="_blank">Open</a>'

        <iframe src="{prj_name}.html" width="500" height="600">
        </iframe>
    </div>
    '''

class VisualFrameTest(VisualTest):
    def __init__(self, test_path, descr,v,v_code,*args):
        iframe = document.createElement('iframe')
        test_name = os.path.split(test_path)[1][:-3]
        title = f'<a href="test.html?s={test_path}&v={v}&v_code={v_code}" target="_blank" >{test_name}</a>'

        iframe.setAttribute('src', f"test.html?s={test_path}&navbar=false&sticky=true&v={v}&v_code={v_code}" )
        iframe.setAttribute('width', 400 + 30)
        iframe.setAttribute('height', 400 + 100)
        iframe.style.overflowX = 'hidden'
        
        super().__init__(title, descr,  iframe, width=420, *args)
        self.test_box.style.minHeight = "550px"
        self.test_box.style.overflowX = "hidden"
        self.visual_wrapper.style.minHeight = "520px"
        self.visual_wrapper.style.overflowX = 'hidden'

#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
#tps._tracing = False
"""
from pyscript import fetch

response = await fetch("test/pyscript-test-generated.json")
if response.ok:
    data = await response.text()
else:
    raise Exception(response.status)

import json
"""

#tpsConfig = json.loads(data)

from pyscript import config 


"""
as tpsConfig

print('tpsConfig', tpsConfig);

test_paths = []
for path in tpsConfig["tps_test_files"]:
    test_paths.append(path);

print('test_paths:', test_paths);
"""




"""
image_gif_tests = [f for name, f 
                     in inspect.getmembers(sys.modules[__name__], inspect.isfunction)
                     if name.startswith('test_image')]

for t in test_paths:
    N += 1
    print("Processing:", t)
    #VisualClickTest(t)
"""



VisualTestSuite(sys.modules[__name__])

#for demo_path in demo_paths:
#   print("Processing demo_path:", demo_path)
#    VisualFrameTest(demo_path, 'pyscript.json')

print('list', list(config['files']))

i = 0
for test_path in config['files']:
    print("Found test_path:", test_path)

    test_path = test_path.replace("{V}", config["files"]["{V}"])
    test_path = test_path.replace("{V_CODE}", config["files"]["{V_CODE}"])

    
    if test_path.startswith('test/uitest_'):
        data = await fetch(test_path).text()
        doc = ast.get_docstring(ast.parse(data))

        VisualFrameTest(test_path.split('?')[0], 
                        doc,
                        config["files"]["{V}"], 
                        config["files"]["{V_CODE}"])
        i += 1
        #if i == 2: break
        