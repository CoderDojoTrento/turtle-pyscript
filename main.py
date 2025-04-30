


from turtleps import *

screen = Screen()
screen.bgpic("img/bg-seaside-2.gif")

iarc =  "img/ch-archeologist-e.gif"  # looks east
screen.register_shape(iarc)

await ge_init()

ada = Sprite()     
ada.goto(-200,0) 
ada.shape(iarc)    
await ada.slide(0,0, 2) 
await ada.say("Hello!", 5)