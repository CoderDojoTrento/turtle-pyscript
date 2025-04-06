from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False


arc = 'img/ch-archeologist-e.gif'
screen = Screen()
screen.register_shape(arc)
await ge_init()


showturtle()
shape(arc)
color('green')
dot(5)
shapesize(3.0)