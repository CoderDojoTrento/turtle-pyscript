   

from turtleps import *

screen = Screen()


hideturtle()

ada = Sprite()

ada.forward(100)

init_engine()

def update():
    
    if pressed("ArrowRight"):
        print("KEY_RIGHT")
        ada.goto(ada.xcor() + 10, ada.ycor())

    if pressed("ArrowLeft"):
        print("KEY_LEFT")
        ada.goto(ada.xcor() - 10, ada.ycor())



    set_timeout(update, interval)    

update()

