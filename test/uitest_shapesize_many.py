""" Shapesizes test

**Polygon shapes**

- small triangle: we only increase **pen**size, notice it bears no effect on the polygon.
- big triangle: we only change **shape**size, notice it also affefts the displayed 
svg `stroke-width`. This is in contrast to original Python turtle 
(see [issue #36](https://github.com/CoderDojoTrento/turtle-pyscript/issues/36)) 
but it's an unavoidable consequence of svg `<use>` def tag.


**Bitmap images**: TODO

**Vector images**: pensize and shapesize don't affect svg `stroke-width` TODO explain better.
"""

from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

arc = 'img/ch-archeologist-e.gif'
tsvg = 'img/turtle.svg'
screen = Screen()
screen.register_shape(arc)
screen.register_shape(tsvg)

await ge_init()

a = Turtle(shape=arc)
a.up()
a.goto(-150,0)
a.down()
a.color('green')
a.dot(5)
#a.shapesize(1.0)

b = Turtle(shape=arc)
b.up()
b.goto(-100,0)
b.down()
b.color('red')
b.dot(5)
b.shapesize(2.0)

c = Turtle(shape=arc)
c.up()
c.goto(0,0)
c.down()
c.color('blue')
c.dot(5)

c.shapesize(1.0, 2.0)

d = Turtle(shape=arc)
d.up()
d.goto(50,0)
d.shapesize(0.5)

e = Turtle(shape=arc)
e.up()
e.goto(100,0)
e.shapesize(2.0,1.0)

p = Turtle(shape=tsvg)
p.up()
p.down()
p.color('lime')
p.dot(5)
p.goto(-100,150)
#p.shapesize(1.0,1.0)

q = Turtle(shape=tsvg)
q.up()
q.goto(100,200)
q.down()
q.color('pink')
q.dot(5)
q.shapesize(-1.0,1.0)

r = Turtle(shape=tsvg)
r.up()
r.goto(-100,-150)
r.down()
r.color('purple')
r.dot(5)
r.shapesize(1.0,-1.0)

w = Turtle(shape=tsvg)
w.up()
w.goto(100,-150)
w.down()
w.color('orange')
w.dot(5)
w.shapesize(-1.0,-1.0)



y = Turtle(shape="triangle")
y.up()
y.goto(150,80)
y.down()
y.shapesize(4)
y.pencolor('red')
y.fillcolor('yellow')

z = Turtle(shape="triangle")
z.down()
z.pensize(10)
z.goto(70,80)
z.pencolor('red')
z.fillcolor('yellow')

