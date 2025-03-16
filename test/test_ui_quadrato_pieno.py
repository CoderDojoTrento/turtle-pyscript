from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

begin_fill()
pencolor('red')
fillcolor('green')
print('pencolor:', pencolor())
print('fillcolor:', fillcolor())

begin_fill()
for i in range(4):
    forward(100)
    await asyncio.sleep(0.5)
    left(90)
    await asyncio.sleep(0.5)
end_fill()