from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

"""from Python official examples (and without transcript done() calls)
"""
up ()
goto (-250, -21)
startPos = pos ()

down ()
color ('red', 'yellow')
begin_fill ()
while True:
    forward (500)

    right (170)

    if distance (startPos) < 1:
        break
end_fill ()
