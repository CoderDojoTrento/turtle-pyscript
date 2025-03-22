from turtleps import *
import urllib

screen = Screen()

# not escaped, works
img1 = r"test/img/a bad %'thing'.gif"

# already escaped, works
#img1 = r"/test/img/a%20bad%20%27thing%27.gif"

# not escaped, doesn't work 
#screen.bgpic(r"/test/img/bg % 'ruins' ò.gif")

# already escaped, works
screen.bgpic(r"/test/img/bg%20%25%20%27ruins%27%20ò.gif")


screen.register_shape(img1)


await ge_init()

a = Sprite()
a.shape(img1)


