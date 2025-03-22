from turtleps import *
import turtleps as tps
import time

import sys
tps._info('python version: ', sys.version)

import pyodide
print("pyodide:", pyodide.__version__)

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

   

await ge_init()

screen = Screen()


ada = Sprite()
bob = Sprite()
ada.fillcolor('pink')
ada.shape('turtle')
bob.shape('arrow')

ts = time.time()


tps._info("Testing slide WITH await")
tps._info("Resetting..")
ada.goto(0,0)
bob.goto(0,0)
tps._info('ada goes sliding...!')
await ada.slide(100,0, 3)
tps._info('ada slide done!')
tps._info('bob goes sliding...!')
await bob.slide(-100,0, 3)
tps._info('bob slide done!')

tps._info("Testing slide WITHOUT await")
tps._info("Resetting..")
ada.goto(0,0)
bob.goto(0,0)
ada.slide(0, 100, 3)
tps._info('ada slide done!')
bob.slide(0, -100, 3)
tps._info('bob slide done!')
