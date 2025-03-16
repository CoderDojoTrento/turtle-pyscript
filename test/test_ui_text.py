from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False
    
color('black', 'white')
dot(10)
color('red')
write("Writing align center", align="center")

goto(-100,100)


color('black', 'white')
dot(10)
color('green')    
write("Writing align left", align="left")

goto(100,-100)
color('black', 'white')
dot(10)
color('blue')
write("Writing align right", align="right")