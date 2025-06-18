
# Use cases

Currently we envision 4 use cases, in order of complexity:

1. single sprite mode
2. multiple sprites mode
3. game engine mode 
4. robotics

**Student target**

4th+ grader with some visual coding skill like with code.org or Scratch
 
- slow at typing, will make errors


## 1. Single sprite mode

**Learning goals**

- student will understand the need to put effort in order to achieve things graphically pleasant
- command sequence concept
- draw squares, rectangles, snowflakes, polygons, waves, ... 
- relative movement, coordinates
- `for` loop, variables, rgb colors

**Requirements**

- user should type the least possible
- user should draw everything from zero
- no default turtle, it confuses students (and defaults are bad anyway)
- slow default speed
- commands like `forward` should be automatically scheduled for execution with `asyncio` without need to explicitly write `await`
  - consider slowing down graphics with svg animations
  - implies we can't use sensing in this mode
- no images are used (in original python Turtle there is support for images but it is so lacking few people use it)
- every action is performed sequentially
- support rgb colors, backgrounds, shapes, compounds, coordinates, writings


## 2. Multiple sprites mode

**Learning goals**

- concurrent programming by drawing some choreography of sprites
- getting accustomed  to concurrent commands and their problems (missing awaits and what not...)
- `def` function 


**Requirements**

- awaitable vs non-awaitable commands
- `asyncio.gather`
- time vs speed parameter: prefer time

## 3. Game engine mode

**Learning goals**

- difference among various image types (bitmap, vectorial)
- developing a non-interactive storytelling animation
- developing an interactive 2d action game, retro arcade style
- image tilting, resizing, reflection 
- input keystrokes difference (immediate vs 'pressed')

**Requirements**

- image `tilt`, `shapesize`
- automatically turned on when user  calls `ge_init()`  (and/or register images?)
- default speed: immediate
- support images for sprites and background
- user input, and 'is_pressed' function #22 
- support `ge_init` for image pre-loading #23 
- every sprite should be assigned to a variable
- need new Sprite class (built on top of `Turtle`)   #19
    - supports comics, easier positioning, ..

**Problems**:  
 
- students take time to choose images

   
## 4. Robotics

Driving some robot with the same turtle commands could be fun, but it's just a dream for now

**Requirements**:

- time vs speed parameter: prefer time
