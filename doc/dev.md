# Dev notes

## Updating screen

### Animations

Prefer `async` function call with a `for` inside instead of SVG anims

**`async` f with `for` inside:**

pros:

- more computationally understandable
- more debuggable
- should be easy to remove and used as answer if given to implement as exercise

cons:

- slower
- less 'webby'

**SVG anims:**

pros:

- more webby
- faster

cons:

- more api to learn



### normal case  (tracing 1)

```
goto
 \- pendown? 
        add node to draw_target    
    update_transform
        \- update svg


circle
    \-  pendown?
        add node to draw_target

shape
  \-change href?
    or substitute with another use node?
```

### not tracing  (tracing 0)

```
goto
 \- pendown? 
        add node to draw_target    <-- should target be:
                                        a. same with display:none (but would hide previous stuff)?
                                        b. another custom target layer for the tracing call with display:none?
                                        c. just the node with display:none?
    update_transform               <-- don't think we should call it
        \- update svg


circle
    \-  pendown?                   
        add node to draw_target    <-- should target be display:none, or just the node?

shape
    update_attrs
        \-change href?                           <--  delay change? when?? 
            or substitute with another use node?   
```

### requestAnimationFrame (tracing 10)

orig tracing(n) doc: only each n-th regular screen update is performed)

This is a delayed drawing, right before the browser paints

```
goto
 \- pendown? 
        add node to draw_target    <-- should target be:
                                        a. same with display:none (but would hide previous stuff)?
                                        b. another custom target layer for the tracing call with display:none?
                                        c. just the node with display:none?
    update_transform               <-- don't think we should call it
        \- update svg

circle
    \-  pendown?                   
        add node to draw_target    <-- should target be display:none, or just the node?

shape
  \-change href?                           <--  delay change? when?? 
    or substitute with another use node?   
```

