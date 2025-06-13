"""Stress tests

## WARNING: these tests can make your system unresponsive..

It may take sometime to load everything ...

"""
import sys 
import os
from pyscript.ffi import create_proxy
from pyscript import document, window, config, fetch
from tps_testing import *
from pyscript import config 


#tps._debugging = False
#tps._debugging = True
#tps._tracing = True
#tps._tracing = False

# TODO TOO MUCH IN COMMON WITH uitests_all, REFACTOR
class VisualFrameTest(VisualTest):
    def __init__(self, test_path, title, descr,v,vc,t,**args):
        iframe = document.createElement('iframe')
        #test_name = os.path.split(test_path)[1][:-3]

        iframe.setAttribute('src', f"test.html?s={test_path}&navbar=false&sticky=true&show_desc=false&show_options=false&t={t}&v={v}&vc={vc}&play_banner=0" )
        iframe.setAttribute('width', 400 + 30)
        iframe.setAttribute('height', 400 + 100)
        iframe.style.overflowX = 'hidden'

        super().__init__(f'<a href="test.html?s={test_path}&t={t}&v={v}&vc={vc}&play_banner=0" target="_blank" >{title}</a>',
                         descr,  
                         iframe, 
                         width=420,
                         title_level=2,
                         **args)
        self.test_box.style.minHeight = "550px"
        self.test_box.style.overflowX = "hidden"
        self.visual_wrapper.style.minHeight = "520px"
        self.visual_wrapper.style.overflowX = 'hidden'


# TODO TOO MUCH IN COMMON WITH uitests_all, REFACTOR
title , desc = await tpsjs.fetch_title_desc('test/uitests_stress.py')
VisualTestSuite(title, desc)

print('list', list(config['files']))

fixed_test_paths = [tp.split('?')[0] for tp in config['files'] if tp.startswith('test/stresstest_')]
fixed_test_paths.sort()

i = 0
for fixed_test_path in fixed_test_paths:
    print("Found test_path:", fixed_test_path)
    
    if fixed_test_path.startswith('test/stresstest_'):
        data = await fetch(fixed_test_path).text()

        title, desc = await tpsjs.fetch_title_desc(fixed_test_path);
        VisualFrameTest(fixed_test_path, 
                        title,
                        desc,
                        config["tps"]["v"], 
                        config["tps"]["vc"],
                        config["tps"]["t"])
        i += 1
        #if i == 2: break
        