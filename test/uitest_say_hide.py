""" Comics pop up show / hide

You should see, in order:

|  time|  what  | duration|
|------|---|--|
|0s|"Hello"|     8|
|2s|turtle disappears|2|
|4s|turtle reappers|2|
|6s|"People!"|2|
|8s|hello finalization is prevented to clear pop up because another pop up is running | |
|10s|"Done!"|2|
|15s|end game||
"""

from turtleps import *
import turtleps as tps

#tps._debugging = False
tps._debugging = True
#tps._tracing = True
tps._tracing = False

tps._info("TEST SAY HIDE: BEGINNING...")

screen = Screen()

await ge_init()

s = Sprite()
s.shape("turtle")
s.shapesize(3)

cs = Sprite()
cs.hide()
cs.goto(150, 150)
cs.pensize(5)
t = 0

async def count():
    font=("Arial", 8, "normal")
    
    for t in range(0,16,1): 
        cs.clear()
        cs.write(f"t={t}", font=("Arial", 25, "normal"))
        await asyncio.sleep(1)
    
async def hello():
    await s.say("Hello",8)
    

async def people():
    tps._info("Going to sleep..")
    await asyncio.sleep(2)
    tps._info("Going to hide()..")
    s.hide()
    tps._info("Going to sleep..")
    await asyncio.sleep(2)
    tps._info("Going to show()..")
    s.show()
    tps._info("Going to sleep..")
    await asyncio.sleep(2)
    tps._info("Going to say()..")
    await s.say("People!", 4)
    await s.say("Done!", 2)    

await asyncio.gather(hello(),
                     people(),
                     count())

tps._info("TEST SAY HIDE: DONE...")