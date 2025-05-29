"""Background all states test

You should see, in order:

0. line drawn by turtle
1. small azure bgpanel, with red outline to signal user shrinked it
2. small seaside, no red border
3. clear(), white, no pic, restores size - detaches turtle
4. full forest
5. set yellow color while having image, nothing seems to happen.
6. set bgpanel, now you should full yellow 
7. detached turtle tries to move, you shouldn't see anything
  
   TODO: in original turtle it doesn't explode nor warns, we should issue warnings
"""


from turtleps import *

async def zz():
    print("Going to sleep..")
    await asyncio.sleep(2)


def bgsquare(color):
    """
    The long, do-it-yourself way for the bgcolor deprived student
    """

    screen = Screen()

    s = Sprite()
    s.hide()
    w = screen._width
    h = screen._height
    s.goto(-w // 2, h // 2)
    s.pendown()
    s.fillcolor(color)
    s.begin_fill()
    for i in range(2):
        s.forward(w)
        s.right(90)
        s.forward(h)
        s.right(90)
    s.end_fill()

#bgsquare('yellow')


screen = Screen()

iseaside = "img/bg-seaside-2.gif" 
screen.register_shape(iseaside)

iforest = "img/bg-forest-1.gif" 
screen.register_shape(iforest)

await ge_init()

screen.background.shapesize(0.5)

# should *not* influence screen border
screen.background.pensize(10)

ada = Sprite()
ada.pendown()
ada.shape("turtle")
ada.pensize(4)
ada.pencolor('green')
ada.forward(200)

print("Putting azure..")
screen.bgcolor('azure')

await zz()

print("Putting small seaside shoudn't reset color..")
screen.background.shape(iseaside)

await zz()
print("clearing screen..")  # note: detaches turtles..
screen.clear()

await zz()
print("Putting small forest..")
screen.background.shape(iforest)

await zz()

print("Color yellow (visually no change)..")
screen.bgcolor('yellow')

await zz()

print("Setting shape bgpanel..")
screen.background.shape('bgpanel')

await zz()

print("Trying to move detached turtle..")
#TODO check turtle is properly detached ...
ada.goto(0,0)
ada.pendown()
ada.goto(100,100)


print("Done!")


