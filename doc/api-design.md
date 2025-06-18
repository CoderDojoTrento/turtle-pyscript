# TurtlePS API design

## Python API
 
- simple
- hackable api
- understandable by students
- close to js/DOM
- close to svg
- basic event system
- never forces to define/extend classes
- doesn't immediately force to define functions
- no decorators magic: explicit is better than implicit
- embrace await/async model




### Original Python Turtle problems

Most important ones first:

1. turtle api is blocking, but to do anything serious in the browser async programming is basically unavoidable  
    - You could use SVG animations but that would mean having the code that runs at fast speed while SVG anim runs slow, if errors pop up it would be difficult for students to relate them to the graphics
2.  default singletons: default Screen,  turtle.  Calling Turtle() directly associates new turtle to default Screen.   
3. complicated method internals: while students are not supposed to care about the internals, it would be nice to have them sufficiently simple to be hackable
4. too much related to Tkinter implementation 
5. default turtle just confuses students, they write `forward()` and forget the sprite `ada.forward()`
6. method names are glued together, like `hideturtle`  (I guess the reason was to avoid underscore but if you want to learn Python you need to use underscore sooner or later..)
7. verbose setters / getters, `setx()`, `xcor()` ...  


### Proposed classes

`Turtle` class should inherit from `Sprite` and be a compat layer for those interested in turtle

```
Sprite  *-1 Videogame   1-*  Screen  ?
   ^
   |
Turtle
```

A Videogame should:

- replace original Turtle Screen?

A Sprite should:

- have no concept of speed, instead provide explicit times allows for more precise coreography 
- should have immediate methods `goto(x,t)` and async methods `await agoto(x,y, t=2)` 
- a `Sprite` should be able to `say` comics (sync, async, ...) 
- emit sounds (maybe stereophonic)?
- a Sprite should be penup by default
- a Sprite should have api with underscores for spell clarity
    a. `hideturtle`  `showturtle` -> `hide` / `show`
    b. should be image focused:  `shapesize` -> `size`,  `pensize` -> `pen_size`
- have simpler x,y properties instead of `goto(xcor()+dx, ycor()+dy)` 

In an educational environment if you want to force students to use `for` loops instead of async ones  you could always erase them from provided template


## await/async model

Question:

start with 

```python
ada.forward(100)
await asyncio.sleep(1)
ada.forward(100)
await asyncio.sleep(1)
ada.left(100)
await asyncio.sleep(1)
```

or some contracted version like

```python
from asyncio import sleep as asleep
ada.forward(100)
await asleep(1)
ada.left(100)
await asleep(1)
ada.forward(100)
await asleep(1)
```


better yet, ad-hoc async methods

Notice `t` can even be a mandatory argument, python doesn't complain if you write it as keyword and helps remind students we're dealing with time-related commands. 

```python
await ada.aforward(100, t=1)
await ada.aleft(100, t=1)
await ada.aforward(100, t=1)
```

