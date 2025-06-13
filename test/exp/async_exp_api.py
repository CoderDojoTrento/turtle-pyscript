import asyncio 
import js


if "pyodide" in sys.modules:
    SYSTEM = "pyodide"
elif sys.implementation.name == "micropython":
    SYSTEM = "micropython"
else:
    raise Exception("Unknown python platform!")


# see https://github.com/CoderDojoTrento/turtle-pyscript/issues/8
_running_tasks = set()

def _schedule_task(awaitable):
    t = asyncio.create_task(awaitable)

    # this is only a CPython problem, see  https://github.com/micropython/micropython/issues/12299
    def clean_task(t):
        if t in _running_tasks:
            _running_tasks.remove(t)
            
    if SYSTEM != "micropython" :
        _running_tasks.add(t)
        t.add_done_callback(clean_task) # consider stop
    
    return t

print("---------- 1. AWAIT ME MAYBE STYLE ----------")

async def _forward(a,t):
    for i in range(3):
        print("  forward by", a/3)
        await asyncio.sleep(t/3)
        
def forward(a,t=0):
    if t == 0:
        print('fast forward ')
    else:
        return _schedule_task(_forward(a,t))

print("fast: ok")
forward(2)             


print("fast: ugly")
forward(2, t=0)  

print("2: wrong")
try:
    await forward(2)       # TypeError: object NoneType can't be used in 'await' expression
except TypeError as e:
    js.console.error(str(e))
    
print("3: ok")
await forward(3, t=1)  # ok

print("4: concurrent")
forward(2, t=1)       # ok ? 

def _play(filepath, t):
        

def play(filepath, t)
    if 
    print("Playing", filepath)

play('sound.mp3')  # play all non-blocking ?
play('sound.mp3', t='end') # play all non-blocking
play('sound.mp3', t=-1)  # play all non-blocking
play('sound.mp3', t=3)  # play 3 secs non-blocking
await play('sound.mp3', t=-1)
await play('sound.mp3', t=3)  # plays for 3 secs


print("---------- 2.  AWAIT ME MAYBE, ALWAYS PROMISE STYLE  ----------")

async def _goto(x,y,t):
    if t == 0:
        print('fast goto ')
        await asyncio.sleep(0)  # just yealds and does nothing else 
    else:
        for i in range(3):
            print("  goto by", a/3)
            await asyncio.sleep(t/3)
        
def goto(x,y,t=0):
    return _schedule_task(_forward(a,t))

print("fast: ok")
goto(2,7)             

print("fast: ugly")
goto(2,7, t=0)  

print("fast: ugly")
await goto(2,7)
    
print("3: ok")
await goto(2,7, t=1)  # ok

print("4: concurrent")
goto(2,7, t=1)       # ok ? 


print("---------- 3.  DOUBLE STYLE  ----------")


def backward(a):
    print('fast backward ')


async def abackward(a, t):
    print('async backward ')
    for i in range(3):
        print("  backward by", a/3)
        await asyncio.sleep(t/3)


async def tbackward(a, t):
    print('async backward ')
    for i in range(3):
        print("  backward by", a/3)
        await asyncio.sleep(t/3)


async def backwardt(a, t):
    print('async backward ')
    for i in range(3):
        print("  backward by", a/3)
        await asyncio.sleep(t/3)

async def tbackward(a, t):
    print('async backward ')
    for i in range(3):
        print("  backward by", a/3)
        await asyncio.sleep(t/3)



print("fast: ok")
backward(2)         


print("fast: wrong")
try:
    backward(2,t=1)        # TypeError: backward() got an unexpected keyword argument 't'
except TypeError as e:
    js.console.error(str(e))


print("fast: wrong")
try:
    await backward(2)       # TypeError: object NoneType can't be used in 'await' expression
except TypeError as e:
    print(e)
    
print(": ok")
await abackward(3, t=1)  # ok

print("4: concurrent")
abackward(2, t=1)       # wrong:  RuntimeWarning: coroutine 'abackward' was never awaited

print("4: concurrent")
try:
    abackward(2)      # TypeError: abackward() missing 1 required positional argument: 't'   
except TypeError as e:
    js.console.error(str(e))




print(": ok")
await tbackward(3, t=1)  # ok

print("4: concurrent")
tbackward(2, t=1)       # wrong

def play(filepath, t):


async def aplay(filepath, t)
    print("Playing", filepath)
    await asyncio.sleep(0.2)

def tplay(filepath, t)
    print("Playing", filepath)
    await asyncio.sleep(0.2)

play('sound.mp3')  # play all non-blocking ?
play('sound.mp3', t='end') # play all non-blocking
play('sound.mp3', t=-1)  # play all non-blocking
play('sound.mp3', t=3)  # play 3 secs non-blocking
await play('sound.mp3', t=-1)
await play('sound.mp3', t=3)  # plays for 3 secs



print('----------------------------------------------')

// https://stackoverflow.com/questions/14412027/can-an-svg-contain-audio-using-javascript
// http://xn--dahlstrm-t4a.net/svg/audio/html5-audio-in-svg.svg

register_shape("img/ada-e.gif") 

vg = VideoGame(width=200, height=500)

ada = Sprite(vg)

imm1 = Image("img/ada-es.gif")
imm2 = Image("img/ada-ew.gif")
imm3 = Image("img/sand.gif")

sound1 = Sound("snd/clap.mp3")
sound2 = Sound("snd/scream.mp3")
sound3 = Sound("snd/scream.mp3")

vg.register(imm1, imm2, imm3, 
            sound1, sound2, sound3)

await vg.load()

sprite1 = Sprite(vg)
sprite1.shape(imm1)

sprite2 = Sprite(vg)
sprite3 = Sprite(vg)


sprite1 = Sprite()
sprite1.shape(imm2)

await sprite1.reproduce(sound1, t=-1)



ada = ge.add_sprite()

def def_shape():
    pass

def def_sound():
    pass

def add_shape():
    pass

def add_sound():
    pass


sprite.shape()




# -------------------------------------------


vg = VideoGame(width=200, height=500)

ada = Sprite(vg)

imm1 = Image(vg, "img/ada-es.gif")
imm2 = Image(vg, "img/ada-ew.gif")
imm3 = Image(vg, "img/sand.gif")

poly1 = Polygon(vg, ((2,3), (1,2), (5,9)))

sound1 = Audio(vg, "snd/clap.mp3")
sound2 = Audio(vg, "snd/scream.mp3")
sound3 = Audio(vg, "snd/scream.mp3")

g = Group(vg, imm1, poly1)


await vg.load()

background = Sprite(vg)
background.rect(0,0,400,400,fill="red", stroke="black")

background.shape(imm3)

sprite1 = Sprite(vg)
sprite1.shape(imm1)

sprite2 = Sprite(vg)
sprite3 = Sprite(vg)


sprite1 = Sprite()
sprite1.shape(imm2)

await sprite1.reproduce(sound1, t=-1)



ada = ge.add_sprite()

def def_shape():
    pass

def def_sound():
    pass

def add_shape():
    pass

def add_sound():
    pass


sprite.shape()

# ---------------------------------

g = Game(width=200, height=500)

g.add("ada1.gif")
g.add("sound1.mp3")
g.add("sfondo1.jpg")

await g.load()

ada = g.add( Sprite() )

ada.shape("ada1.gif")
ada.goto(200,0)
ada.size(-1.0, 1.0)   # aka turtle shapesize
ada.pensize(2)           # turtle pensize

sfondo = g.background()
sfondo.fillcolor()
#sfondo.shape("sfondo1.jpg")
#sfondo.size(2.0,1.2)


# if failed, suggest spellings...



background = Sprite(vg)
background.rect(0,0,400,400,fill="red", stroke="black")

background.shape(imm3)

sprite1 = Sprite(vg)
sprite1.shape(imm1)

sprite2 = Sprite(vg)
sprite3 = Sprite(vg)


sprite1 = Sprite()
sprite1.shape(imm2)

await sprite1.reproduce(sound1, t=-1)



ada = ge.add_sprite()

def def_shape():
    pass

def def_sound():
    pass

def add_shape():
    pass

def add_sound():
    pass


sprite.shape()
