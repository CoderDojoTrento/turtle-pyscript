from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False


pensize(5)
up()
goto(-200,-110)
down()
pencolor(255,0,0)
forward(100)
pencolor((0,255,0))
forward(100)
pencolor((0,0,255))
forward(100)
pencolor('purple')
forward(100)
print('pencolor:', pencolor())
print('fillcolor:', fillcolor())

pencolor('yellow')
fillcolor(255,0,0)

up()
goto(-50,0)
down()
begin_fill()
for i in range(4):
    forward(50)
    left(90)
end_fill()

pencolor('cyan')
fillcolor((0,255,0))

up()
goto(0,-50)
down()
begin_fill()
for i in range(4):
    forward(50)
    left(90)
end_fill()

pencolor('orange')
fillcolor((0,0,255))

up()
goto(50,0)
down()
begin_fill()
for i in range(4):
    forward(50)
    left(90)
end_fill()

pencolor('grey')
fillcolor('purple')

up()
goto(0,50)
down()
begin_fill()
for i in range(4):
    forward(50)
    left(90)
end_fill()