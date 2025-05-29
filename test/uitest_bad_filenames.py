""" Bad filenames test

To keep things straightforward we don't do any processing of the urls, which is left to the user.

Expected result: unescaped urls won't be properly loaded and a couple warning signs should show instead.
Hovering on the warning signs you should see the error cause.
"""

from turtleps import *

screen = Screen()


# already escaped, works
imge1 = r"test/img/a%20bad%20%25%27thing%27.gif"

# already escaped, works
imge2 = r"test/img/bg%20%25%20%27ruins%27%20ò.gif"

# not escaped, doesn't work
imgb1 = r"test/img/a bad %'thing'.gif"

# not escaped, doesn't work
imgb2 = r"test/img/bg % 'ruins' ò.gif"



screen.register_shape(imge1)

screen.register_shape(imge2)

screen.register_shape(imgb1)

screen.register_shape(imgb2)


await ge_init()

screen.background.shape(imge2)

a = Sprite()
a.goto(-150,0)
a.shape(imge1)


b = Sprite()
b.goto(0,0)
b.shape(imgb1)


c = Sprite()
c.goto(150,0)
c.shape(imgb2)
