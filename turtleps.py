# ************             ATTENZIONE!                ******************** 
# ************    _NON_ SCRIVERE IN QUESTO FILE !!    ********************
#


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

#_debugging = False
_debugging = True
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


_CFG = {"width" : 0.5,               # Screen
        "height" : 0.75,
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
        "resizemode" : "noresize",
        "visible" : True,
        "language": "english",        # docstrings
        "exampleturtle": "turtle",
        "examplescreen": "screen",
        "title": "Python Turtle Graphics",
        "using_IDLE": False
       }


_ns = 'http://www.w3.org/2000/svg'
_svg = document.createElementNS (_ns, 'svg')
_defs = document.createElementNS (_ns, 'defs')
_defs.setAttributeNS(None, 'id', 'defs')
_svg.appendChild(_defs)

# so we can at least define z-order of turtles
_svg_turtles = document.createElementNS (_ns, 'g')
_svg_turtles.setAttribute('class', 'turtles')
_svg_painting = document.createElementNS (_ns, 'g')
_svg_painting.setAttribute('class', 'painting')


_svg.appendChild(_svg_painting)
_svg.appendChild(_svg_turtles)



_defaultElement = document.getElementById ('__turtlegraph__')
if not _defaultElement:
    _defaultElement = document.body
_defaultElement.appendChild (_svg)


_width = None
_height = None
_offset = None


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
            img.setAttributeNS(None, 'x', 0)
            img.setAttributeNS(None, 'y', 0)
            img.setAttributeNS(None, 'width', 20)
            img.setAttributeNS(None, 'height', 20)
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


class Screen:
    def __init__(self):
        _debug("CDTN: Initializing screen...")
        self.svg = _svg
        self.svg_turtles = _svg_turtles
        self.svg_painting = _svg_painting
        
        self._turtles = []
        self._shapes = {}

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
        self.svg_turtles.replaceChildren()
        self.svg_painting.replaceChildren()
        
        #for btn in 1, 2, 3:
        #    self.onclick(None, btn)
        #self.onkeypress(None)
        #for key in self._keys[:]:
        #    self.onkey(None, key)
        #    self.onkeypress(None, key)
        #Turtle._pen = None
        


    def setup(self, width=_CFG["width"], height=_CFG["height"],
              startx=_CFG["leftright"], starty=_CFG["topbottom"]):
        """ Set the size and position of the main window.

        Arguments:
        width: as integer a size in pixels, as float a fraction of the screen.
          Default is 50% of screen.
        height: as integer the height in pixels, as float a fraction of the
          screen. Default is 75% of screen.
        startx: if positive, starting position in pixels from the left
          edge of the screen, if negative from the right edge
          Default, startx=None is to center window horizontally.
        starty: if positive, starting position in pixels from the top
          edge of the screen, if negative from the bottom edge
          Default, starty=None is to center window vertically.

        Examples (for a Screen instance named screen):
        >>> screen.setup (width=200, height=200, startx=0, starty=0)

        sets window to 200x200 pixels, in upper left of screen

        >>> screen.setup(width=.75, height=0.5, startx=None, starty=None)

        sets window to 75% of screen by 50% of screen and centers
        """
        """
        if not hasattr(self._root, "set_geometry"):
            return
        sw = self._root.win_width()
        sh = self._root.win_height()
        if isinstance(width, float) and 0 <= width <= 1:
            width = sw*width
        if startx is None:
            startx = (sw - width) / 2
        if isinstance(height, float) and 0 <= height <= 1:
            height = sh*height
        if starty is None:
            starty = (sh - height) / 2
        self._root.set_geometry(width, height, startx, starty)
        """
        
        
        self.update()

    def update(self):
        """Perform a TurtleScreen update.
        """
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
        # TODO check double registration   

        _debug(f"CDTN: Registering shape: name: {name}   shape:{shape}")
        

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
            

_defaultScreen = Screen()


#def _rightSize (self):
def _rightSize(self=None):
    global _width
    global _height
    global _offset

    _width = _defaultElement.offsetWidth
    _height = _defaultElement.offsetHeight
    _offset = [_width // 2, _height // 2]

    _svg.setAttribute('width', _width)
    _svg.setAttribute('height', _height)

window.onresize = _rightSize

#_rightSize ()
#CDTN TODO TypeError: _rightSize() missing 1 required positional argument: 'self'
_rightSize()

def bgcolor(*args):
    _defaultScreen.bgcolor(*args)

bgcolor('white')

def setDefaultElement(element):
    global _defaultElement

    _defaultElement.removeChild(_svg)
    _defaultElement = element
    element.appendChild(_svg)

    _rightSize()
    bgcolor('white')

_allTurtles = []

class Turtle:

    def __init__(self, 
                 shape=_CFG["shape"],  # NOTE: this is meant to be an id
                 visible=_CFG["visible"]):
        
        
        _allTurtles.append (self)

        self._position = [0,0] 
        self._paths = []
        self._track = []
        
        self._pencolor = _CFG["pencolor"]
        self._fillcolor = _CFG["fillcolor"]
        self._pensize = 1

        self._shown = True
        self._fill = False
        self._heading = 0
        
        self.screen = _defaultScreen
        self.screen._turtles.append(self)

        #shape_node = document.getElementById(shape)
        #cloned_shape_node = shape_node.cloneNode(True)
        #self.screen.svg.appendChild(cloned_shape_node)

        use_node = document.createElementNS (_ns, 'use')
        use_node.setAttribute('id', f"turtle-{id(self)}")

        """
        <use href="#tree" x="50" y="100" />  
        """
        
        self.svg = use_node

        self.screen.svg_turtles.appendChild(use_node)
        _debug("turtle was appended to screen.svg_turtles")

        self.shape(shape)

        self.reset()
        _trace(f"{self._heading=}")

    def _svg_transform(self):

        shape_el = document.getElementById(self._shape)
        tilt_fix = 0
        if shape_el.tagName == 'polygon':
            tilt_fix = -90   # polygons are designed pointing top, images look natural pointing right :-/
            _trace(f"{tilt_fix=}")

        rot = math.degrees(-self._heading) + tilt_fix
        _trace(f"{rot=}")
        return f"translate({self._position[0] + _offset[0]},{self._position[1] + _offset[1]}) rotate({rot})"

    def _create_track(self):
        _debug("Creating new _track_svg_path")
        self._track = []    # Need to make track explicitly because
        # _track should start with a move command
        self._track.append('{} {} {}'.format(
            'M',
            self._position[0] + _offset[0],
            self._position[1] + _offset[1])
        )

        tsp = document.createElementNS(_ns, 'path')
                
        self.screen.svg_painting.appendChild(tsp)
        self._paths.append(tsp)
        self._track_svg_path = tsp

    def reset(self):
        self._heading = 0
        self.down ()
        self.color ('black', 'black')
        self.pensize (1)

        self.home()         # Makes a position but needs a track to put in
        self.clear()        # Makes a track but needs a position to initialize it with


       
    def clear(self):
        _debug("Clearing turtle...")
        for path in self._paths:
            self.screen.svg_painting.removeChild(path)
        self._paths = []  # TODO rename, it hosts anything drawn by the turtle

        self._create_track()
        self._moveto(self._position)

    def _flush(self):
        
        _debug('Flush:', self._track)

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

    def pensize(self, width):
        #self._flush()
        if width == None:
            return self._pensize
        else:
            self._pensize = width

    def color(self, pencolor, fillcolor = None):
        #self._flush()
        self.pencolor(pencolor)

        if fillcolor is not None:
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


    def goto(self, x, y = None):
        if y is None:
            self._position = x
        else:
            self._position = [x, y]

        self._track.append('{} {} {}'.format(
            'L' if self._down else 'M',
            self._position[0] + _offset[0],
            self._position[1] + _offset[1])
        )

        self._update_transform()
        self._flush()

    def _moveto(self, x, y = None):
        wasdown = self.isdown()
        self.up()
        self.goto(x, y)
        if wasdown:
            self.down()

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

    def _predict(self, length):
        corrected_heading = self._heading + math.pi/2
        delta = [math.sin(corrected_heading), math.cos(corrected_heading)]
        return [self._position[0] + length * delta[0], self._position[1] + length * delta[1]]

    def forward(self, length):
        self._position = self._predict(length)

        self._track.append('{} {} {}'.format(
            'L' if self._down else 'M',
            self._position[0] + _offset[0],
            self._position[1] + _offset[1])
        )
        self._update_transform()
        self._flush()

    def back(self, length):
        self.forward(-length)

    

    def circle(self, radius):
        self.left(90)
        opposite = self._predict(2 * (radius + 1) + 1)
        self.right(90)

        self._track.append('{} {} {} {} {} {} {} {}'.format(
            'A',
            radius,
            radius,
            0,
            1,
            0,
            opposite[0] + _offset[0],
            opposite[1] + _offset[1]
        ))

        self._track.append('{} {} {} {} {} {} {} {}'.format(
            'A',
            radius,
            radius,
            0,
            1,
            0,
            self._position[0] + _offset[0],
            self._position[1] + _offset[1]
        ))
        self._flush()

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
        self.svg.setAttribute('transform', self._svg_transform())

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
        #tsp.setAttribute('fill-rule', 'evenodd') # don't think we need it
        self._fill = False
        self._create_track()
        
        
    def speed(self, speed=None):
        """ Return or set the turtle's speed.

        Optional argument:
        speed -- an integer in the range 0..10 or a speedstring (see below)

        Set the turtle's speed to an integer value in the range 0 .. 10.
        If no argument is given: return current speed.

        If input is a number greater than 10 or smaller than 0.5,
        speed is set to 0.
        Speedstrings  are mapped to speedvalues in the following way:
            'fastest' :  0
            'fast'    :  10
            'normal'  :  6
            'slow'    :  3
            'slowest' :  1
        speeds from 1 to 10 enforce increasingly faster animation of
        line drawing and turtle turning.

        Attention:
        speed = 0 : *no* animation takes place. forward/back makes turtle jump
        and likewise left/right make the turtle turn instantly.

        Example (for a Turtle instance named turtle):
        >>> turtle.speed(3)
        """
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
    
    def write(self, arg, move=False, align="left", font=("Arial", 8, "normal")):
        """Write text at the current turtle position.

        Arguments:
        arg -- info, which is to be written to the TurtleScreen
        move (optional) -- True/False
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
        """
        <text x="20" y="35" class="small">My</text>
        """
        txt = document.createElementNS (_ns, 'text')
        txt.setAttribute('x', self._position[0] + _offset[0])
        txt.setAttribute('y', self._position[1] + _offset[1])
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
                    alignment-baseline:central;
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
        if not name in self.screen.getshapes():
            raise TurtleGraphicsError("There is no registered shape named %s" % name)
        self._shape = name
        shape_svg_id = f'#{name}'

        self.svg.setAttribute('href', shape_svg_id)
        #use_node.setAttribute('x', 0 + _offset[0])  # setting this prevents polygon rotation from working
        #use_node.setAttribute('y', 0 + _offset[1])
        
        shape_el = document.getElementById(name)

        if shape_el.tagName == 'polygon':
            self.svg.setAttribute('fill', _CFG["fillcolor"])
            self.svg.setAttribute('stroke', _CFG["pencolor"])
            self.svg.setAttribute('stroke-width', 1)
            self.svg.setAttribute('fill-rule', 'evenodd')

        self.svg.setAttribute('transform', self._svg_transform())

        #self._update()

    fd = forward
    bk = back
    backward = back
    rt = right
    lt = left
    ht = hideturtle
    setpos = goto
    setposition = goto
    seth = setheading
    up = penup
    pu = penup
    down = pendown
    



_defaultTurtle = Turtle()
_timer = None

def reset():
    global _timer, _allTurtles
    if _timer:
        clearTimeout(_timer)
    bgcolor('white')
    for turtle in _allTurtles:
        turtle.reset()
        turtle._flush()

def clear():
    global _allTurtles
    for turtle in _allTurtles:
        turtle.clear()

def ontimer(fun, t = 0):
    global _timer
    _timer = setTimeout(fun, t)


def pensize(width):                    _defaultTurtle.pensize(width)
def color(pencolor, fillcolor = None): _defaultTurtle.color(pencolor, fillcolor)
def home():                            _defaultTurtle.home()
def goto(x, y = None):                 _defaultTurtle.goto(x, y)
def position(): return _defaultTurtle.position()
def pos(): return _defaultTurtle.pos()
def xcor(): return _defaultTurtle.xcor()
def ycor(): return _defaultTurtle.ycor()


def distance(x, y = None): return _defaultTurtle.distance(x, y)
def penup():                              _defaultTurtle.penup()
def pendown():                            _defaultTurtle.pendown()

def up():                              _defaultTurtle.penup()
def down():                            _defaultTurtle.pendown()
def forward(length):                   _defaultTurtle.forward(length)
def back(length):                      _defaultTurtle.back(length)
def circle(radius):                    _defaultTurtle.circle(radius)
def left(angle):                       _defaultTurtle.left(angle)
def right(angle):                      _defaultTurtle.right(angle)
def begin_fill():                      _defaultTurtle.begin_fill()
def end_fill():                        _defaultTurtle.end_fill()
def speed(speed):                      _defaultTurtle.speed(speed)
def setheading(angle):                 _defaultTurtle.setheading(angle)
def hideturtle():                      _defaultTurtle.hideturtle()
def ht():                      _defaultTurtle.hideturtle()
def pencolor(*args):           _defaultTurtle.pencolor(*args)
def fillcolor(*args):          _defaultTurtle.fillcolor(*args)
def bgcolor(*args):      _defaultTurtle.bgcolor(*args) 

fd = forward
bk = back
backward = back
rt = right
lt = left
setpos = goto
setposition = goto
seth = setheading



"""

Coderdojo Trento Game Engine

Very minimal game engine which adds some convenience on top of turtleps
Stuff is added only as functions on purpose, to avoid class stuff.

Eventually, what follows will go into a separate file
"""


#from turtleps import *
import asyncio


class CDTNException(Exception):
    pass

""" Some renaming, turtle everywhere can get confusing
"""
class Sprite(Turtle):
    pass


def carica_immagine(sprite, immagine):
    sprite.screen.register_shape(immagine)
    sprite.shape(immagine)

async def dire(sprite, testo, tempo, dx=0, dy=65):
    tfumetto = Turtle()
    sprite.screen.tracer(0)
    tfumetto.speed(0)
    tfumetto.hideturtle()
    tfumetto.forward(0) # should bring it to front but in trinket it doesnt :-/
    fontsize = 10
    carw = 0.6 * fontsize
    base = (len(testo)+2)*carw
    alt = 20
    tfumetto.penup()
    x = sprite.xcor() + dx
    y = sprite.ycor() + dy
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
    tfumetto.color("white")
    tfumetto.setheading(0)
    tfumetto.begin_fill()
    for i in range(2):
        tfumetto.forward(base)
        tfumetto.right(90)
        tfumetto.forward(alt)
        tfumetto.right(90)
    tfumetto.end_fill()
    tfumetto.penup()
    tfumetto.color("black")
    tfumetto.forward(base / 2)
    tfumetto.right(90)
    tfumetto.forward(fontsize*1.5)
    tfumetto.write(testo,
                    align="center",
                    font=('Arial', fontsize, 'normal'))
    
    sprite.screen.tracer(1)
    await asyncio.sleep(tempo)
    tfumetto.clear()


async def test_turtleps():
    _info("TEST TURTLEPS: BEGINNING...")
    #ada = Turtle(shape='img/turtle.svg')
    ada = Turtle()

    #await asyncio.sleep(1)

    #for i in range(3):
    ada.color('green')
    await dire(ada, "Ciao!", 3)


    ada.write("Ciao mondo!", align="right", font=("Courier", 18, "bold"))
    ada.forward(100)
    #time.sleep(1)
    #await asyncio.sleep(1)
    
    ada.left(90)

    #time.sleep(1)
    
    ada.circle(40)
    
    ada.forward(100)

    ada.color('blue')
    ada.write("La la", align="center", font=("Times New Roman", 24, "italic"))
    ada.left(90)
    ada.forward(100)
    
    _info("TEST TURTLEPS: DONE...")

async def test_fumetti():

    _info("TEST FUMETTI: BEGINNING...")
    t = Sprite()
    t.speed(10)
    carica_immagine(t, 'ch-archeologist1.gif')
    
    await dire(t, "abcdefghilmnopqrstuvzABCDEFGHILMNOPQRSTUVZ",2)
    await dire(t, "Più in alto",2, dy = 120)
    await dire(t, "Più in basso",2, dy = -120)
    await dire(t, "Più a destra",2, dx = 120)
    await dire(t, "Più a sinistra",2, dx = -120)
    
    await dire(t, "Ciao1", 1)
    t.goto(-250, 0)
    await dire(t, "Ciao2", 1)
    t.goto(250, 0)
    await dire(t, "Ciao3", 1)
    t.goto(0, 250)
    await dire(t, "Ciao4", 1)
    t.goto(0, -250)
    await dire(t, "Ciao5", 1)
    t.goto(250, -250)
    await dire(t, "Ciao6", 1)
    t.goto(-250, 250)
    await dire(t, "Ciao7", 1)
    t.goto(-250, -250)
    await dire(t, "Ciao8", 1)
    t.goto(250, 250)
    await dire(t, "Ciao9", 1)
    
    _info("TEST FUMETTI: DONE...")

def test_big_star():
    """from Python official examples (and without transcript done() calls)
    """
    up ()
    goto (-250, -21)
    startPos = pos ()

    down ()
    color ('red', 'yellow')
    begin_fill ()
    while True:
        forward (500)

        right (170)

        if distance (startPos) < 1:
            break
    end_fill ()

def test_colors():
    pensize(5)
    up()
    goto(-200,-110)
    down()
    pencolor(255,0,0)
    forward(100)
    pencolor((0,255,0))
    forward(100)
    pencolor((0,0,255))
    forward(100)
    pencolor('purple')
    forward(100)
    print('pencolor:', pencolor())
    print('fillcolor:', fillcolor())

    pencolor('yellow')
    fillcolor(255,0,0)

    up()
    goto(-50,0)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()

    pencolor('cyan')
    fillcolor((0,255,0))

    up()
    goto(0,-50)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()

    pencolor('orange')
    fillcolor((0,0,255))

    up()
    goto(50,0)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()

    pencolor('grey')
    fillcolor('purple')

    up()
    goto(0,50)
    down()
    begin_fill()
    for i in range(4):
        forward(50)
        left(90)
    end_fill()


def test_quadrato_pieno():
    begin_fill()
    pencolor('red')
    fillcolor('green')
    print('pencolor:', pencolor())
    print('fillcolor:', fillcolor())

    begin_fill()
    for i in range(4):
        forward(100)
        left(90)
    end_fill()

"""
screen = Screen()

if hasattr(screen, "colormode"):
    #print("Setting screen.colormode to 255")
    screen.colormode(255)  # this is Trinket default, see https://github.com/CoderDojoTrento/turtle-storytelling/issues/2
"""

