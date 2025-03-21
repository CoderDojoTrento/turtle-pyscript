from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

for i in range(500):
    forward(100)
    left(90)
    color('red')  # should create a new path

