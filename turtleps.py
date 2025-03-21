# ************             ATTENZIONE!                ******************** 
# ************    _NON_ SCRIVERE IN QUESTO FILE !!    ********************
#

from pyodide.ffi.wrappers import add_event_listener
import uuid


"""
Aug 2024:
TURTLE MODULE TAKEN FROM transcrypt (apache licence)

https://github.com/TranscryptOrg/Transcrypt/blob/master/transcrypt/modules/turtle/__init__.py

NOTE: YOU DON'T NEED TRANSCRIPT, WE EXECUTE IT IN PYSCRIPT
"""

# not importing anything from turtle as it's disabled in pyodide

class TurtleGraphicsError(Exception):
    """Some TurtleGraphics Error
    """ 
    pass

class Vec2D(tuple):
    """A 2 dimensional vector class, used as a helper class
    for implementing turtle graphics.
    May be useful for turtle graphics programs also.
    Derived from tuple, so a vector is a tuple!

    Provides (for a, b vectors, k number):
       a+b vector addition
       a-b vector subtraction
       a*b inner product
       k*a and a*k multiplication with scalar
       |a| absolute value of a
       a.rotate(angle) rotation
    """
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
    def __add__(self, other):
        return Vec2D(self[0]+other[0], self[1]+other[1])
    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0]*other[0]+self[1]*other[1]
        return Vec2D(self[0]*other, self[1]*other)
    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0]*other, self[1]*other)
        return NotImplemented
    def __sub__(self, other):
        return Vec2D(self[0]-other[0], self[1]-other[1])
    def __neg__(self):
        return Vec2D(-self[0], -self[1])
    def __abs__(self):
        return math.hypot(*self)
    def rotate(self, angle):
        """rotate self counterclockwise by angle
        """
        perp = Vec2D(-self[1], self[0])
        angle = math.radians(angle)
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0]*c+perp[0]*s, self[1]*c+perp[1]*s)
    def __getnewargs__(self):
        return (self[0], self[1])
    def __repr__(self):
        return "(%.2f,%.2f)" % self


def _parse_color_args(*args):
    if len(args) == 1:
        if isinstance(args[0], tuple):
            svg_color = f"rgb({','.join([str(a) for a in args[0]])})"
        elif isinstance(args[0], str):
            svg_color = args[0]
        else:
            raise TurtleGraphicsError(f"Unrecognized color format: {args[0]}")    
    elif len(args) == 3:
        svg_color = f"rgb({','.join([str(a) for a in args])})"
    else:
        raise TurtleGraphicsError(f"Unrecognized color format: {args}")
    return svg_color

from js import (
    document,
    window
)


#__pragma__ ('skip')
#document = Math = setInterval = clearInterval = 0
#__pragma__ ('noskip')

import math

_debugging = False
#_debugging = True
#_tracing = True
_tracing = False

def _debug(*args):
    if _debugging:
        print("DEBUG:",*args)

def _trace(*args):
    if _tracing:
        print("TRACE:",*args)
        
def _info(*args):
    print("INFO:", *args)

def _warn(*args):
    print("WARN:", *args)



#def abs (vec2D):
#    return Math.sqrt (vec2D [0] * vec2D [0] + vec2D [1] * vec2D [1])


_CFG = {"width" : 400, # 0.5,               # Screen
        "height" : 400, # 0.75,
        "canvwidth" : 400,
        "canvheight": 300,
        "leftright": None,
        "topbottom": None,
        "mode": "standard",          # TurtleScreen
        "colormode": 1.0,
        "delay": 10,
        "undobuffersize": 1000,      # RawTurtle
        "shape": "classic",
        "pencolor" : "black",
        "fillcolor" : "black",
        "resizemode" : "noresize",   # CDTN: why? I would expect "user"
        "visible" : True,
        "language": "english",        # docstrings
        "exampleturtle": "turtle",
        "examplescreen": "screen",
        "title": "Python Turtle Graphics",
        "using_IDLE": False
       }


_ns = 'http://www.w3.org/2000/svg'
_svg = document.createElementNS (_ns, 'svg')

_svg.style.setProperty('border-style','solid')
_svg.style.setProperty('border-color','lightgrey')


_defs = document.createElementNS (_ns, 'defs')
_defs.setAttributeNS(None, 'id', 'defs')
_svg.appendChild(_defs)

# so we can at least define z-order of turtles
_svg_sprites = document.createElementNS (_ns, 'g')
_svg_sprites.setAttribute('class', 'sprites')
_svg_painting = document.createElementNS (_ns, 'g')
_svg_painting.setAttribute('class', 'painting')


_svg.appendChild(_svg_painting)
_svg.appendChild(_svg_sprites)



_defaultElement = document.getElementById ('__turtlegraph__')
if not _defaultElement:
    _defaultElement = document.body

_defaultElement.appendChild (_svg)
""" CDTN: The _svg container
"""



class Shape(object):
    """Data structure modeling shapes.

    attribute _type is one of "polygon", "image", "compound"
    attribute _data is - depending on _type a poygon-tuple,
    an image or a list constructed using the addcomponent method.
    
    CDTN: doesn't seem really useful, in the original CPython implementation doesn't 
          have public attributes nor methods to retrieve stuff. 
          original _data  che be in many forms, from concrete bitmap images to tuples
          Decision: will store in ._data nothing
                    will store in .svg an unlinked svg element 
          
    """
    
    def __init__(self, type_, data=None):
        self._type = type_
        
    
        if type_ == "polygon":
            
            if isinstance(data, list):
                data = tuple(data)
                """
                <polygon points="100,100 150,25 150,75 200,0" fill="none" stroke="black" />
                """
            
            poly = document.createElementNS(_ns, 'polygon')
            points_str = ' '.join([','.join([str(el) for el in t]) for t in data])
            poly.setAttributeNS(None, 'points', points_str)
            self.svg = poly
            
            # leaving default fill...
            
        elif type_ == "image":
            if not data:
                raise ValueError("CDTN: Missing image data!")

            img = document.createElementNS(_ns, 'image')
            #img.setAttributeNS(None, 'x', 0)
            #img.setAttributeNS(None, 'y', 0)
            #img.setAttributeNS(None, 'width', 20)
            #img.setAttributeNS(None, 'height', 20)
            #img.setAttributeNS(None, 'xlink:href', name)  # doesn't like it
            img.setAttributeNS(None, 'href', data)
            
            self.svg = img 

            #CDTN commented, expect svg node
            #if isinstance(data, str):
                #if data.lower().endswith(".gif") and os.path.isfile(data):
                #   data = TurtleScreen._image(data)
            
                # else data assumed to be PhotoImage  # CDTN ??

        elif type_ == "compound":
            #data = []  CDTN
            self.svg = document.createElementNS(_ns, 'g')   # group
        else:
            raise TurtleGraphicsError("There is no shape type %s" % type_)
        
    def get_svg_image_size(self):
        """
        """
        if self._type != "image":
            raise CDTNException("Other types are currently not supported")
        _debug(f"{window.getComputedStyle(self.svg).getPropertyValue('width')=}")   # '50.3px'
        _debug(f"{window.getComputedStyle(self.svg).getPropertyValue('height')=}")  # '50.5px'
        cs = window.getComputedStyle(self.svg)
        return(float(cs.getPropertyValue('width')[:-2]), float(cs.getPropertyValue('height')[:-2]))

        #_debug(f"{self.svg_shape.getBBox()=}")
        #_debug(f"{self.svg_shape.getBBox()["width"]=}")  # wtf  TypeError: 'pyodide.ffi.JsProxy' object is not subscriptable
        #_debug(f"{self.svg_shape.getBBox()[2]=}")                     # no
        #_debug(f'{self.svg_shape.getBBox().getProperty("width")=}')   # no
        #_debug(f'{self.svg_shape.getBBox().getAttribute("width")=}')  # no
        


    def addcomponent(self, poly, fill, outline=None):
        """Add component to a shape of type compound.

        Arguments: poly is a polygon, i. e. a tuple of number pairs.
        fill is the fillcolor of the component,
        outline is the outline color of the component.

        call (for a Shapeobject namend s):
        --   s.addcomponent(((0,0), (10,10), (-10,10)), "red", "blue")

        Example:
        >>> poly = ((0,0),(10,-5),(0,10),(-10,-5))
        >>> s = Shape("compound")
        >>> s.addcomponent(poly, "red", "blue")
        >>> # .. add more components and then use register_shape()
        """
        if self._type != "compound":
            raise TurtleGraphicsError("Cannot add component to %s Shape"
                                                                % self._type)
        if outline is None:
            outline = fill
       
        poly = document.createElementNS(_ns, 'polygon')
        points_str = ' '.join([','.join(t) for t in data])
        poly.setAttributeNS(None, 'points', points_str)
        if fill:
            poly.setAttributeNS(None, 'fill', fill)
        
        if outline:
            poly.setAttributeNS(None, 'outline', outline)
        
        self._data.appendChild(poly)

def Screen():
    """Return the singleton screen object.
    If none exists at the moment, create a new one and return it,
    else return the existing one."""
    if Turtle._screen is None:
        _debug("No default screen found, creating one..")
        Turtle._screen = _Screen()
    return Turtle._screen

class _Screen:
    def __init__(self):
        _debug("CDTN: Initializing screen...")
        self.svg = _svg
        self.svg_sprites = _svg_sprites
        self.svg_painting = _svg_painting
        self._bgpicname = ''
        self._timer = None

        self._turtles = []
        self._shapes = {}

        self._width = _CFG["width"]
        self._height = _CFG["height"]
        self._offset = [_CFG["width"]//2, _CFG["height"]//2]


        #self.canvwidth = w
        #self.canvheight = h
        #self.xscale = self.yscale = 1.0

        shapes = {
                   "arrow" : Shape("polygon", ((-10,0), (10,0), (0,10))),
                  "turtle" : Shape("polygon", ((0,16), (-2,14), (-1,10), (-4,7),
                              (-7,9), (-9,8), (-6,5), (-7,1), (-5,-3), (-8,-6),
                              (-6,-8), (-4,-5), (0,-7), (4,-5), (6,-8), (8,-6),
                              (5,-3), (7,1), (6,5), (9,8), (7,9), (4,7), (1,10),
                              (2,14))),
                  "circle" : Shape("polygon", ((10,0), (9.51,3.09), (8.09,5.88),
                              (5.88,8.09), (3.09,9.51), (0,10), (-3.09,9.51),
                              (-5.88,8.09), (-8.09,5.88), (-9.51,3.09), (-10,0),
                              (-9.51,-3.09), (-8.09,-5.88), (-5.88,-8.09),
                              (-3.09,-9.51), (-0.00,-10.00), (3.09,-9.51),
                              (5.88,-8.09), (8.09,-5.88), (9.51,-3.09))),
                  "square" : Shape("polygon", ((10,-10), (10,10), (-10,10),
                              (-10,-10))),
                "triangle" : Shape("polygon", ((10,-5.77), (0,11.55),
                              (-10,-5.77))),
                  "classic": Shape("polygon", ((0,0),(-5,-9),(0,-7),(5,-9))),
                   #CDTN not supported "blank" : Shape("image", self._blankimage())
                  }
        for name, shape in shapes.items():
            self.register_shape(name, shape)

        self._bgpics = {"nopic" : ""}

        #self._mode = mode
        #self._delayvalue = delay
        #self._colormode = _CFG["colormode"]
        #self._keys = []
        self.clear()
        #if sys.platform == 'darwin':
            # Force Turtle window to the front on OS X. This is needed because
            # the Turtle window will show behind the Terminal window when you
            # start the demo from the command line.
        #    rootwindow = cv.winfo_toplevel()
        #    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
        #    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')

        def _right_size(myself=None):
            self.update()
            self.setup()

        
        window.onresize = _right_size
        _right_size()


        self._defaultTurtle = Turtle(screen=self)

    
    def getshapes(self):
        """Return a list of names of all currently available turtle shapes.

        No argument.

        Example (for a TurtleScreen instance named screen):
        >>> screen.getshapes()
        ['arrow', 'blank', 'circle', ... , 'turtle']
        """
        return sorted(self._shapes.keys())

    def clear(self):
        """Delete all drawings and all turtles from the TurtleScreen.

        No argument.

        Reset empty TurtleScreen to its initial state: white background,
        no backgroundimage, no eventbindings and tracing on.

        Example (for a TurtleScreen instance named screen):
        >>> screen.clear()

        Note: this method is not available as function.
        """
        _debug("Screen.clear()")

        #self._delayvalue = _CFG["delay"]
        #self._colormode = _CFG["colormode"]
        #self._delete("all")
        #self._bgpic = self._createimage("")
        #self._bgpicname = "nopic"
        #self._tracing = 1
        #self._updatecounter = 0
        #self._turtles = []
        
        self.bgcolor("white")
        self.svg_sprites.replaceChildren()
        self.svg_painting.replaceChildren()
        
        #for btn in 1, 2, 3:
        #    self.onclick(None, btn)
        #self.onkeypress(None)
        #for key in self._keys[:]:
        #    self.onkey(None, key)
        #    self.onkeypress(None, key)
        #Turtle._pen = None
        


    def setup(self, width=_CFG["width"], height=_CFG["height"]):
        
        #self.svg.setAttribute('viewBox', f'200 200 {width} {height}')
        self._width  = width
        self._height = height
        
        self.update()

    def update(self):
        """Perform a TurtleScreen update.
        """
        #self._width = _defaultElement.offsetWidth
        #self._height = _defaultElement.offsetHeight
        self._offset = [self._width // 2, self._height // 2]

        self.svg.setAttribute('width', self._width)
        self.svg.setAttribute('height', self._height)        
        
        #tracing = self._tracing
        #self._tracing = True
        #for t in self.turtles():
        #    t._update_data()
        #    t._drawturtle()
        #self._tracing = tracing
        #self._update()
        pass
        

    def register_shape(self, name, shape=None):
        """Adds a turtle shape to TurtleScreen's shapelist.

        Arguments:
        (1) name is the name of a gif-file and shape is None.
            Installs the corresponding image shape.
            !! CDTN: images in our implementation do actually turn to heading orientation
        (2) name is an arbitrary string and shape is a tuple
            of pairs of coordinates. Installs the corresponding
            polygon shape
        (3) name is an arbitrary string and shape is a
            (compound) Shape object. Installs the corresponding
            compound shape.
        To use a shape, you have to issue the command shape(shapename).

        call: register_shape("turtle.gif")
        --or: register_shape("tri", ((0,0), (10,10), (-10,10)))

        Example (for a TurtleScreen instance named screen):
        >>> screen.register_shape("triangle", ((5,-3),(0,5),(-5,-3)))

        """

        _debug(f"CDTN: Registering shape: name: {name}   shape:{shape}")
        
        if name in self._shapes:
            _warn(f"Screen.register_shape(): trying to register the same shape twice: {name}   ")

        defs = self.svg.getElementById("defs")
        
        if shape is None:
            the_shape = Shape("image", name)

        elif isinstance(shape, tuple):
            the_shape = Shape("polygon", shape)
        else:
            the_shape = shape
            
        # else shape assumed to be Shape-instance


        # TODO sanitize?
        the_shape.svg.setAttributeNS(None, 'id', name)

        defs.appendChild(the_shape.svg)
        self._shapes[name] =  the_shape
        
    def bgpic(self, picname=None):
        """Set background image or return name of current backgroundimage.

        Optional argument:
        picname -- a string, name of a gif-file or "nopic".

        If picname is a filename, set the corresponding image as background.
        If picname is "nopic", delete backgroundimage, if present.
        If picname is None, return the filename of the current backgroundimage.

        Example (for a TurtleScreen instance named screen):
        >>> screen.bgpic()
        'nopic'
        >>> screen.bgpic("landscape.gif")
        >>> screen.bgpic()
        'landscape.gif'
        """
        if picname is None:
            return self._bgpicname
        self._bgpicname = picname
        _debug(f"Setting background-image {picname}")
        self.svg.style.setProperty('background-image', f'url({picname})')


    def _window_size(self):
        """ Return the width and height of the turtle window.
        """
        #width = self.cv.winfo_width()
        #if width <= 1:  # the window isn't managed by a geometry manager
        #    width = self.cv['width']
        #height = self.cv.winfo_height()
        #if height <= 1: # the window isn't managed by a geometry manager
        #    height = self.cv['height']
        
        bcr = self.svg.getBoundingClientRect()
        
        return bcr['width'], bcr['height']

    def window_width(self):
        """ Return the width of the turtle window.

        Example (for a TurtleScreen instance named screen):
        >>> screen.window_width()
        640
        """
        return self._window_size()[0]

    def window_height(self):
        """ Return the height of the turtle window.

        Example (for a TurtleScreen instance named screen):
        >>> screen.window_height()
        480
        """
        return self._window_size()[1]
    
    def _iscolorstring(self, color):
        """Check if the string color is a legal SVG color string.
        """
        #CDTN TODO Too optimistic
        return True
 
    
    

    def tracer(self, n=None, delay=None):
        """Turns turtle animation on/off and set delay for update drawings.

        Optional arguments:
        n -- nonnegative  integer
        delay -- nonnegative  integer

        If n is given, only each n-th regular screen update is really performed.
        (Can be used to accelerate the drawing of complex graphics.)
        Second arguments sets delay value (see RawTurtle.delay())

        Example (for a TurtleScreen instance named screen):
        >>> screen.tracer(8, 25)
        >>> dist = 2
        >>> for i in range(200):
        ...     fd(dist)
        ...     rt(90)
        ...     dist += 2
        """
        _warn("Turtle.tracer() is currently *NOT IMPLEMENTED*")
        """
        if n is None:
            return self._tracing
        self._tracing = int(n)
        self._updatecounter = 0
        if delay is not None:
            self._delayvalue = int(delay)
        if self._tracing:
            self.update()
        """

    def bgcolor(self, *args):
        if len(args) == 0:
            return self._bgcolor
        
        if len(args) == 0:
            return self.svg.style["background-color"] 
        else:
            s = _parse_color_args(*args)    
            self.svg.style.setProperty("background-color",  s)
            

    def reset(self):
        if self._timer:
            clearTimeout(self._timer)   # js
        self.bgcolor('white')
        for turtle in self._turtles:
            turtle.reset()
            turtle._flush()

    def clear(self):
        for turtle in self._turtles:
            turtle.clear()

    def ontimer(fun, t = 0):
        global _timer
        _timer = setTimeout(fun, t)   # js



class Turtle:

    _screen = None

    def __init__(self, 
                 screen=None,
                 shape=_CFG["shape"],  # NOTE: this is meant to be an id
                 visible=_CFG["visible"]):
        
        _debug("A new Turtle is born!")

        if not screen:
            screen = Turtle._screen

        self.screen = screen
        self.screen._turtles.append(self)


        self._position = [0,0] 
        self._stretchfactor = (1., 1.)
        self._paths = []   # TODO rename, it hosts anything drawn by the turtle
        self._track = []
        
        self._pencolor = _CFG["pencolor"]
        self._fillcolor = _CFG["fillcolor"]
        self._pensize = 1

        self._shown = True
        self._fill = False
        self._heading = 0.0
        self._tilt = 0
        
        

        #shape_node = document.getElementById(shape)
        #cloned_shape_node = shape_node.cloneNode(True)
        #self.screen.svg.appendChild(cloned_shape_node)

        group_node = document.createElementNS (_ns, 'g')
        use_node = document.createElementNS (_ns, 'use')
        
        group_node.setAttribute('id', f"sprite-{id(self)}")

        """
        <use href="#tree" x="50" y="100" />  
        """
        
        self.svg = group_node
        self.svg_shape = use_node

        group_node.appendChild(use_node)
        self.screen.svg_sprites.appendChild(group_node)
        _debug("turtle was appended to screen.svg_sprites")

        self.shape(shape)

        self.reset()
        _trace(f"{self._heading=}")


    

    def _create_track(self):
        _debug("Creating new _track_svg_path")
        self._track = []    # Need to make track explicitly because
        # _track should start with a move command
        self._track.append('{} {} {}'.format(
            'M',
            self._position[0] + self.screen._offset[0],
            self.screen._offset[1] - self._position[1])
        )

        tsp = document.createElementNS(_ns, 'path')
        tsp.setAttribute('fill', 'none')           
        tsp.setAttribute('fill-rule', 'nonzero')     
            
        self.screen.svg_painting.appendChild(tsp)
        self._paths.append(tsp)
        self._track_svg_path = tsp

    def reset(self):
        self._heading = 0.0
        self._tilt = 0.0
        self._stretchfactor = (1., 1.)
        self.down ()
        self.color ('black', 'black')
        self.pensize (1)

        self.home()         # Makes a position but needs a track to put in
        self.clear()        # Makes a track but needs a position to initialize it with


       
    def clear(self):
        _debug("Clearing turtle...")
        for path in self._paths:
            self.screen.svg_painting.removeChild(path)
        self._paths = []  
        self._create_track()
        self._moveto(self._position)

    def _flush(self):
        
        _trace('Flush:', self._track)

        if len(self._track) > 1:
            tsp = self._track_svg_path
            ts = ' '.join (self._track)
            ds = tsp.getAttribute('d')

            _debug(f"{ds=}")
            if ds:
                ts = f"{ds} {ts}"
            _debug(f"{ts=}")
            tsp.setAttribute('d', ts)
            tsp.setAttribute('stroke', self._pencolor if self._pencolor != None else 'none')
            tsp.setAttribute('stroke-width', self._pensize)
                

    #def done(self):
    #    self._flush()

    def pensize(self, width=None):
        
        if width == None:
            return self._pensize
        else:
            self._pensize = width

    def color(self, pencolor, fillcolor = None):
        
        self.pencolor(pencolor)

        if fillcolor is None:
            self.fillcolor(pencolor)

        else:
            self.fillcolor(fillcolor)

    def _colorstr(self, color):
        """Return color string corresponding to args.

        Argument may be a string or a tuple of three
        numbers corresponding to actual colormode,
        i.e. in the range 0<=n<=colormode.

        If the argument doesn't represent a color,
        an error is raised.
        """
        if len(color) == 1:
            color = color[0]
        if isinstance(color, str):
            if self._iscolorstring(color) or color == "":
                return color
            else:
                raise TurtleGraphicsError("bad color string: %s" % str(color))
        try:
            r, g, b = color
        except (TypeError, ValueError):
            raise TurtleGraphicsError("bad color arguments: %s" % str(color))
        if self._colormode == 1.0:
            r, g, b = [round(255.0*x) for x in (r, g, b)]
        if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
            raise TurtleGraphicsError("bad color sequence: %s" % str(color))
        return "#%02x%02x%02x" % (r, g, b)

    def _color(self, cstr):
        if not cstr.startswith("#"):
            return cstr
        if len(cstr) == 7:
            cl = [int(cstr[i:i+2], 16) for i in (1, 3, 5)]
        elif len(cstr) == 4:
            cl = [16*int(cstr[h], 16) for h in cstr[1:]]
        else:
            raise TurtleGraphicsError("bad colorstring: %s" % cstr)
        return tuple(c * self._colormode/255 for c in cl)

    def pencolor(self, *args):
        
        if len(args) == 0:
            return self._pencolor
        else:
            s = _parse_color_args(*args)
            self._pencolor = s
            self.svg.style.setProperty("background-color",  s)
            self._create_track()   # CDTN TODO hack so we can show path with segments of different colors

    def fillcolor(self, *args):
        if len(args) == 0:
            return self._fillcolor
        else:
            s = _parse_color_args(*args)
            self._fillcolor = s
            #TODO change some svg property??



    def home(self):
        self._moveto(0, 0)

    def position(self):
        #TODO CDTN self._position should natively be a Vec2D
        return Vec2D(self._position[0], self._position[1]) 

    def pos(self):
        return self.position()
    
    def xcor(self):
        return self._position[0]
    
    def ycor(self):
        return self._position[1]
    

    def distance(self, x, y = None):
        if y is None:
            other = x
        else:
            other = [x, y]

        dX = other[0] - self._position[0]
        dY = other[1] - self._position[1]

        return math.sqrt (dX * dX + dY * dY)

    def penup(self):
        self._down = False

    def pendown(self):
        self._down = True

    def isdown(self): 
        return self._down

    def goto(self, x_or_pair, y = None):
        """Move turtle to an absolute position.

        Arguments:
        x -- a number      or     a pair/vector of numbers
        y -- a number             None
        """
        if y is None:
            self._position = x_or_pair
        else:
            self._position = [x_or_pair, y]


        if self._down:
            _trace("goto: self._down")
            self._track.append('{} {} {}'.format(
                'L' if self._down else 'M',
                self._position[0] + self.screen._offset[0],
                self.screen._offset[1] - self._position[1])
            )
            self._flush()

        self._update_transform()

    def _moveto(self, x, y = None):
        wasdown = self.isdown()
        self.up()
        self.goto(x, y)
        if wasdown:
            self.down()


    def _predict(self, length):
        corrected_heading = self._heading + math.pi/2
        delta = [math.sin(corrected_heading), math.cos(corrected_heading)]
        return [self._position[0] + length * delta[0], self._position[1] - length * delta[1]]

    def forward(self, length):
        self._position = self._predict(length)

        if self._down:
            _trace("goto: self._down")

            self._track.append('{} {} {}'.format(
                'L' if self._down else 'M',
                self._position[0] + self.screen._offset[0],
                self.screen._offset[1] - self._position[1])   
            )
            self._flush()

        self._update_transform()
        
    def back(self, length):
        self.forward(-length)



    def stamp(self):
        """Stamp a copy of the turtleshape onto the canvas and return its id.

        No argument.

        Stamp a copy of the turtle shape onto the canvas at the current
        turtle position. 
        Example (for a Turtle instance named turtle):
        >>> turtle.color("blue")
        >>> turtle.stamp()
        """
        # TODO Return a stamp_id for that stamp, which can be
        # used to delete it by calling clearstamp(stamp_id).

        the_id = f"stamp-{uuid.uuid4()}"
        cloned = self.svg.cloneNode(True)
        cloned.setAttribute("id", the_id)
        self.screen.svg_painting.appendChild(cloned)
        return the_id

    def dot(self, radius):
        """
        <circle cx="50" cy="50" r="50" />
        """
        dot = document.createElementNS (_ns, 'circle')
        dot.setAttribute('cx', self._position[0] + self.screen._offset[0])
        dot.setAttribute('cy', self.screen._offset[1] - self._position[1])
        dot.setAttribute('r', radius)
        dot.setAttribute('fill', self._fillcolor)
        dot.setAttribute('stroke', self._pencolor)
        dot.setAttribute('stroke-width', self._pensize)

        self.screen.svg_painting.appendChild(dot)
        self._paths.append(dot)

    def circle(self, radius):
        """
        <circle cx="50" cy="50" r="50" />
        """
        circle = document.createElementNS (_ns, 'circle')
        circle.setAttribute('cx', self._position[0] + self.screen._offset[0])
        circle.setAttribute('cy', self.screen._offset[1] - self._position[1] )
        circle.setAttribute('r', radius)
        circle.setAttribute('fill', 'none')
        circle.setAttribute('stroke', self._pencolor)
        circle.setAttribute('stroke-width', self._pensize)
        self.screen.svg_painting.appendChild(circle)
        self._paths.append(circle)


    def heading(self):
        """ Return the turtle's current heading.

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.left(67)
        >>> turtle.heading()
        67.0
        """
        return math.degrees(self._heading)
    
    def _update_transform(self):
        """ This *seems* to work
        <g transform="translate(200,200)">
            <use id="sprite-11056328"
             href="#img/ch-archeologist-e.gif" 
             transform="rotate(90.0) scale(4.0,4.0)" 
             transform-origin="20 30"></use>
        </g>
        """
        shape = self.screen._shapes[self._shape]
        
        tilt_fix = 0
        if shape._type == 'polygon':
            tilt_fix = -math.pi/2   # polygons are designed pointing top, images look natural pointing right :-/
            _trace(f"{tilt_fix=}")

        rot = math.degrees(-self._heading - self._tilt + tilt_fix) 
        _trace(f"{rot=}")
        scale = f"{self._stretchfactor[0]},{self._stretchfactor[1]}"
        translate = f"{self._position[0] + self.screen._offset[0]},{self.screen._offset[1] - self._position[1]}"

        self.svg.setAttribute('transform',f"translate({translate})")
        self.svg_shape.setAttribute('transform', 
                                    f"rotate({rot}) scale({scale})")
        
        
        if shape._type == "image":
            size = shape.get_svg_image_size()
            self.svg_shape.setAttribute('transform', 
                                        f"translate(-{size[0] // 2}, -{size[1] // 2}) rotate({rot}) scale({scale})")
        
            self.svg_shape.setAttribute('transform-origin',f'{size[0] // 2} {size[1] // 2}'); 
        else:
            #TODO manage polygon and compound cases
            pass

    def setheading(self, to_angle):
        """Set the orientation of the turtle to to_angle.

        Aliases:  setheading | seth

        Argument:
        to_angle -- a number (integer or float)

        Set the orientation of the turtle to to_angle.
        Here are some common directions in degrees:

         standard - mode:          logo-mode:
        -------------------|--------------------
           0 - east                0 - north
          90 - north              90 - east
         180 - west              180 - south
         270 - south             270 - west

        Example (for a Turtle instance named turtle):
        >>> turtle.setheading(90)
        >>> turtle.heading()
        90
        """
        self._heading =  (to_angle * math.pi / 180.0) % (2 * math.pi)
        self._update_transform()

    def tiltangle(self, angle=None):
        """Set or return the current tilt-angle.

        Optional argument: angle -- number

        Rotate the turtleshape to point in the direction specified by angle,
        regardless of its current tilt-angle. DO NOT change the turtle's
        heading (direction of movement).
        If angle is not given: return the current tilt-angle, i. e. the angle
        between the orientation of the turtleshape and the heading of the
        turtle (its direction of movement).

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("circle")
        >>> turtle.shapesize(5, 2)
        >>> turtle.tiltangle()
        0.0
        >>> turtle.tiltangle(45)
        >>> turtle.tiltangle()
        45.0
        >>> turtle.stamp()
        >>> turtle.fd(50)
        >>> turtle.tiltangle(-45)
        >>> turtle.tiltangle()
        315.0
        >>> turtle.stamp()
        >>> turtle.fd(50)
        """
        if angle is None:
            return math.degrees(self._tilt)
        else:
            self._tilt = math.radians(angle) % (math.pi*2)
            self._update_transform()

    def tilt(self, angle):
        """Rotate the turtleshape by angle.

        Argument:
        angle - a number

        Rotate the turtleshape by angle from its current tilt-angle,
        but do NOT change the turtle's heading (direction of movement).

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("circle")
        >>> turtle.shapesize(5,2)
        >>> turtle.tilt(30)
        >>> turtle.fd(50)
        >>> turtle.tilt(30)
        >>> turtle.fd(50)
        """
        self.tiltangle(angle + self.tiltangle())

    def left(self, angle):
        _trace(f"left: prev heading {self._heading}")
        
        self._heading = (self._heading + (angle * math.pi / 180.0)) % (2 * math.pi)
        
        _trace(f"    : new heading {self._heading}")
        self._update_transform()

    def right(self, angle): 
        self.left(-angle)

    def begin_fill(self):
        _debug("Beginning fill")
        self._create_track()
        self._fill = True

    def end_fill(self):
        _debug("end_fill")
        tsp = self._track_svg_path
        tsp.setAttribute('fill', self._fillcolor if self._fill and self._fillcolor != None else 'none')           
        tsp.setAttribute('fill-rule', 'nonzero') 
        self._fill = False
        self._create_track()
        
        
    def speed(self, speed=None):
        
        _warn("Turtle.speed is not implemented yet")
        
        """
        speeds = {'fastest':0, 'fast':10, 'normal':6, 'slow':3, 'slowest':1 }
        if speed is None:
            return self._speed
        if speed in speeds:
            speed = speeds[speed]
        elif 0.5 < speed < 10.5:
            speed = int(round(speed))
        else:
            speed = 0
        self.pen(speed=speed)
        """

    def shapesize(self, stretch_wid=None, stretch_len=None):
        if stretch_wid is stretch_len is None:
            stretch_wid, stretch_len = self._stretchfactor
            return stretch_wid, stretch_len
        if stretch_wid == 0 or stretch_len == 0:
            raise TurtleGraphicsError("stretch_wid/stretch_len must not be zero")
        if stretch_wid is not None:
            if stretch_len is None:
                stretchfactor = stretch_wid, stretch_wid
            else:
                stretchfactor = stretch_wid, stretch_len
        elif stretch_len is not None:
            stretchfactor = self._stretchfactor[0], stretch_len
        else:
            stretchfactor = self._stretchfactor
    
        self._stretchfactor = stretchfactor
        self._update_transform()

    def write(self, arg, align="left", font=("Arial", 8, "normal")):
        """Write text at the current turtle position.

        Arguments:
        arg -- info, which is to be written to the TurtleScreen
        align (optional) -- one of the strings "left", "center" or right"
        font (optional) -- a triple (fontname, fontsize, fonttype)

        Write text - the string representation of arg - at the current
        turtle position according to align ("left", "center" or right")
        and with the given font.
        If move is True, the pen is moved to the bottom-right corner
        of the text. By default, move is False.

        Example (for a Turtle instance named turtle):
        >>> turtle.write('Home = ', True, align="center")
        >>> turtle.write((0,0), True)
        """
        #CDTN missing boolean move argument
        """
        <text x="20" y="35" class="small">My</text>
        """
        txt = document.createElementNS (_ns, 'text')
        txt.setAttribute('x', self._position[0] + self.screen._offset[0])
        txt.setAttribute('y', self.screen._offset[1] - self._position[1])
        txt.textContent = arg

        #for now let's use text-anchor https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-anchor
        if align == "left":
            text_anchor = "end"
        elif align == "center":
            text_anchor = "middle"
        elif align == "right":
            text_anchor = "start"
        else:
            raise ValueError(f"Unknown align: {align}")
        
        style = f"""font-family: {font[0]}; 
                    font-weight: {font[2]};
                    font-size: {font[1]}px; 
                    fill: {self._pencolor};
                    text-anchor:{text_anchor};
                    #alignment-baseline:central; #different in Turtle!
                    alignment-baseline:baseline;   
        """
        txt.setAttribute('style',  style)
        
        self.screen.svg_painting.appendChild(txt)
        self._paths.append(txt)

        """
        if self.undobuffer:
            self.undobuffer.push(["seq"])
            self.undobuffer.cumulate = True
        end = self._write(str(arg), align.lower(), font)
        if move:
            x, y = self.pos()
            self.setpos(end, y)
        if self.undobuffer:
            self.undobuffer.cumulate = False
        """


    def showturtle(self):
        """Makes the turtle visible.

        Aliases: showturtle | st

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.hideturtle()
        >>> turtle.showturtle()
        """
        self.svg.setAttribute('visibility', 'visible')

        #self.pen(shown=True)

    def hideturtle(self):
        """Makes the turtle invisible.

        Aliases: hideturtle | ht

        No argument.

        It's a good idea to do this while you're in the
        middle of a complicated drawing, because hiding
        the turtle speeds up the drawing observably.

        Example (for a Turtle instance named turtle):
        >>> turtle.hideturtle()
        """
        self.svg.setAttribute('visibility', 'hidden')
        self._shown = False
        #self.pen(shown=False)



    def isvisible(self):
        """Return True if the Turtle is shown, False if it's hidden.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.hideturtle()
        >>> print(turtle.isvisible())
        False
        """
        return self._shown

    def shape(self, name=None):
        """Set turtle shape to shape with given name / return current shapename.

        Optional argument:
        name -- a string, which is a valid shapename

        Set turtle shape to shape with given name or, if name is not given,
        return name of current shape.
        Shape with name must exist in the TurtleScreen's shape dictionary.
        Initially there are the following polygon shapes:
        'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'.
        To learn about how to deal with shapes see Screen-method register_shape.

        Example (for a Turtle instance named turtle):
        >>> turtle.shape()
        'arrow'
        >>> turtle.shape("turtle")
        >>> turtle.shape()
        'turtle'
        """
        if name is None:
            return self._shape
        _debug(f"Setting turtle shape to {name}")
        if not name in self.screen.getshapes():
            raise TurtleGraphicsError("There is no registered shape named %s" % name)
        self._shape = name
        shape_svg_id = f'#{name}'

        self.svg_shape.setAttribute('href', shape_svg_id)
        #use_node.setAttribute('x', 0 + self.screen._offset[0])  # setting this prevents polygon rotation from working
        #use_node.setAttribute('y', 0 + self.screen._offset[1])
        
        shape_el = document.getElementById(name)

        if shape_el.tagName == 'polygon':
            self.svg_shape.setAttribute('fill', _CFG["fillcolor"])
            self.svg_shape.setAttribute('stroke', _CFG["pencolor"])
            self.svg_shape.setAttribute('stroke-width', 1)
            self.svg_shape.setAttribute('fill-rule', 'evenodd')

        self._update_transform()

        #self._update()

    fd = forward
    bk = back
    backward = back
    rt = right
    lt = left
    ht = hideturtle
    st = showturtle  
    setpos = goto
    setposition = goto
    seth = setheading
    up = penup
    pu = penup
    down = pendown
    turtlesize = shapesize    



def pensize(width=None):                    return Turtle._screen._defaultTurtle.pensize(width)
def color(pencolor, fillcolor = None): Turtle._screen._defaultTurtle.color(pencolor, fillcolor)
def home():                            Turtle._screen._defaultTurtle.home()
def goto(x, y = None):                 Turtle._screen._defaultTurtle.goto(x, y)
def position(): return Turtle._screen._defaultTurtle.position()
def pos(): return Turtle._screen._defaultTurtle.pos()
def xcor(): return Turtle._screen._defaultTurtle.xcor()
def ycor(): return Turtle._screen._defaultTurtle.ycor()


def distance(x, y = None): return Turtle._screen._defaultTurtle.distance(x, y)
def penup():                              Turtle._screen._defaultTurtle.penup()
def pendown():                            Turtle._screen._defaultTurtle.pendown()

def up():                              Turtle._screen._defaultTurtle.penup()
def down():                            Turtle._screen._defaultTurtle.pendown()
def forward(length):                   Turtle._screen._defaultTurtle.forward(length)
def back(length):                      Turtle._screen._defaultTurtle.back(length)
def circle(radius):                    Turtle._screen._defaultTurtle.circle(radius)
def left(angle):                       Turtle._screen._defaultTurtle.left(angle)
def right(angle):                      Turtle._screen._defaultTurtle.right(angle)
def begin_fill():                      Turtle._screen._defaultTurtle.begin_fill()
def end_fill():                        Turtle._screen._defaultTurtle.end_fill()
def heading():                         return Turtle._screen._defaultTurtle.heading() 
def tiltangle(angle=None):             return Turtle._screen._defaultTurtle.tiltangle(angle)
def tilt(angle):                       return Turtle._screen._defaultTurtle.tilt(angle) 

def speed(speed):                      return Turtle._screen._defaultTurtle.speed(speed)
def setheading(angle):                 Turtle._screen._defaultTurtle.setheading(angle)
def hideturtle():                      Turtle._screen._defaultTurtle.hideturtle()
def ht():                      Turtle._screen._defaultTurtle.hideturtle()
def showturtle():                      Turtle._screen._defaultTurtle.showturtle()
def stamp():                      return Turtle._screen._defaultTurtle.stamp()

def st():                      Turtle._screen._defaultTurtle.showturtle()
def pencolor(*args):           return Turtle._screen._defaultTurtle.pencolor(*args)
def fillcolor(*args):          return Turtle._screen._defaultTurtle.fillcolor(*args)
def shapesize(stretch_wid=None, stretch_len=None):          Turtle._screen._defaultTurtle.shapesize(stretch_wid, stretch_len)
def shape(name=None): return Turtle._screen._defaultTurtle.shape(name)
def dot(radius):     Turtle._screen._defaultTurtle.dot(radius)
def circle(radius):     Turtle._screen._defaultTurtle.circle(radius)
def write(arg, align="left", font=("Arial", 8, "normal")): Turtle._screen._defaultTurtle.write(arg, align=align, font=font)


fd = forward
bk = back
backward = back
rt = right
lt = left
setpos = goto
setposition = goto
seth = setheading
turtlesize = shapesize


Turtle._screen = Screen()
Turtle._screen.setup(400,400)

def bgcolor(*args):
    Turtle._screen.bgcolor(*args)

bgcolor('white')

"""
def setDefaultElement(element):
    global _defaultElement

    _defaultElement.removeChild(_svg)
    _defaultElement = element
    element.appendChild(_svg)

    _rightSize()
    bgcolor('white')
"""



"""

Coderdojo Trento Game Engine

Very minimal game engine which adds some convenience on top of turtleps
Stuff is added only as functions on purpose, to avoid class stuff.

Eventually, what follows will go into a separate file
"""


#from turtleps import *
import asyncio

async def ge_init():
    """ Waits until all images and resources are loaded
    """
    hideturtle()  # dont need it in most games..
    # TODO set speed 0 ?
    await asyncio.sleep(0.5)  # TODO horror

class CDTNException(Exception):
    pass

""" Some renaming, turtle everywhere can get confusing
"""
class Sprite(Turtle):

    def __init__( self, 
                  screen=None,
                  shape=_CFG["shape"],        # NOTE: this is meant to be an id
                  visible=_CFG["visible"]):
        super().__init__(screen, shape, visible)
        self.penup()  # no need for pen in most videogames..

    def hide(self):
        self.hideturtle()

    def show(self):
        self.showturtle()


    def _load_image(self, image):
        """ Experimental, should be awaitable, don't use it...
        """
        screen = Screen()
        screen.register_shape(image)
        self.shape(image)

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, value: float):
        self.goto(value, self._position[1])

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, value: float):
        self.goto(self._position[0], value)

    def to_foreground(self):

        self.screen.svg_sprites.removeChild(self.svg)
        self.screen.svg_sprites.appendChild(self.svg)

    def to_background(self):
        ss = self.screen.svg_sprites
        ss.removeChild(self.svg)

        if len(self.screen._turtles) > 0:
            ss.insertBefore(self.svg, ss.children[0])
        else: 
            ss.appendChild(self.svg)


    async def say(self, text, seconds, dx=0, dy=65):
        #if dy == None:
            #_debug(f"sprite.svg")
            #_debug(f"{sprite.svg.getBBox()=}")
            
            #dy = sprite.svg.getBBox().height()  # gives weird TypeError int 
            #_debug(f"{dy=}")
        
        tfumetto = Turtle()
        #self.screen.tracer(0) # TODO
        tfumetto.speed(0)
        tfumetto.hideturtle()
        tfumetto.forward(0) # should bring it to front but in trinket it doesnt :-/
        fontsize = 15
        carw = 0.5 * fontsize
        base = (len(text)+2)*carw
        alt = 28
        tfumetto.penup()
        x = self.xcor() + dx - base//3
        y = self.ycor() + dy
        if x + base > 200:
            x = 200 - base
        if y + alt > 200:
            y = 200
        if x < -200:
            x = -200
        if y < -200 + alt:
            y = -200 + alt
        tfumetto.goto(x, y)
        tfumetto.pendown()
        tfumetto.pencolor("black")
        tfumetto.fillcolor("white")
        
        tfumetto.setheading(0)
        tfumetto.begin_fill()
        for i in range(2):
            tfumetto.forward(base)
            tfumetto.right(90)
            tfumetto.forward(alt)
            tfumetto.right(90)
        tfumetto.end_fill()
        tfumetto.penup()
        tfumetto.color("black", "white")
        tfumetto.forward(base / 2)
        tfumetto.right(90)
        tfumetto.forward(fontsize*1.2)
        tfumetto.write(text,
                    align="center",
                    font=('Arial', fontsize, 'normal'))
        
        #self.screen.tracer(1)  # TODO
        await asyncio.sleep(seconds)
        tfumetto.clear()

    async def slide(sprite, x, y, seconds=1):
        """ Slowly moves toward a point in a given time. Note this function is async.
        """
        frames = seconds * ge_framerate
        sides = x - sprite.x, y - sprite.y
        delta_space = (sides[0] / frames), (sides[1] / frames)
        _debug(f"{delta_space}=")
        _debug(f"{sprite.x}=")
        for i in range(frames):
            sprite.x += delta_space[0]            
            sprite.y += delta_space[1]
            await asyncio.sleep(ge_frame_interval)



"""
screen = Screen()

if hasattr(screen, "colormode"):
    #print("Setting screen.colormode to 255")
    screen.colormode(255)  # this is Trinket default, see https://github.com/CoderDojoTrento/turtle-storytelling/issues/2
"""


# VERY DRAFTY EVENT LOOP STUFF

import random
#import pyscript.web.dom
from pyscript import when, display
from pyscript.web import page, img

from js import DOMParser
from js import (
    document,
    Element,
)

from pyscript import window, document

from pyodide.http import open_url
from pyodide.ffi.wrappers import set_timeout
from pyodide.ffi.wrappers import add_event_listener
import asyncio



ctx = None

ge_framerate = 60
ge_frame_interval = (1 / ge_framerate)  # secs


_pressedKeys = {
}


def _handle_input(e):
    """ {
     "key": "a",
     "keyCode": 65,
     "which": 65,
     "code": "KeyA",
     "location": 0,
     "altKey": false,
     "ctrlKey": false,
     "metaKey": false,
     "shiftKey": false,
     "repeat": false
    }

    {
     "key": "ArrowLeft",
     "keyCode": 37,
     "which": 37,
     "code": "ArrowLeft",
     "location": 0,
     "altKey": false,
     "ctrlKey": false,
     "metaKey": false,
     "shiftKey": false,
     "repeat": false
    }
    """
    global _pressedKeys
    if e.type == "keydown":
        _pressedKeys[e.key] = True
    elif e.type == "keyup":
        _pressedKeys[e.key] = False

def pressed(key: str):
    if key in _pressedKeys:
        return _pressedKeys[key]
    else:
        return False


def init_engine():
    #TODO this function probably is not needed

     #init input
    add_event_listener(
        document,
        "keydown",
        _handle_input
    )

    add_event_listener(
        document,
        "keyup",
        _handle_input
    )
    