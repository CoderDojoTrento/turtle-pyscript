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

from js import (
    document,
    window
)


#__pragma__ ('skip')
#document = Math = setInterval = clearInterval = 0
#__pragma__ ('noskip')

import math

#_debug = False
_debug = True


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
        print("CDTN: Initializing screen...")
        self.svg = _svg
        self._turtles = []
        
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

    def clear(self):
        """Delete all drawings and all turtles from the TurtleScreen.

        No argument.

        Reset empty TurtleScreen to its initial state: white background,
        no backgroundimage, no eventbindings and tracing on.

        Example (for a TurtleScreen instance named screen):
        >>> screen.clear()

        Note: this method is not available as function.
        """
        #self._delayvalue = _CFG["delay"]
        #self._colormode = _CFG["colormode"]
        #self._delete("all")
        #self._bgpic = self._createimage("")
        #self._bgpicname = "nopic"
        #self._tracing = 1
        #self._updatecounter = 0
        #self._turtles = []
        self.bgcolor("white")
        self.svg.replaceChildren()
        self.svg.appendChild(_defs)
        #for btn in 1, 2, 3:
        #    self.onclick(None, btn)
        #self.onkeypress(None)
        #for key in self._keys[:]:
        #    self.onkey(None, key)
        #    self.onkeypress(None, key)
        #Turtle._pen = None
        pass


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

        print(f"CDTN: Registering shape: name: {name}   shape:{shape}")
        

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
        """Check if the string color is a legal Tkinter color string.
        """
        #CDTN TODO Too optimistic
        return True
    
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

    
    def _bgcolor(self, color=None):
        """Set canvas' backgroundcolor if color is not None,
        else return backgroundcolor."""
    
        if color:
            self.svg.style.setProperty("background-color",  color)
        else:
            return self.svg.style["background-color"] 
        
    def bgcolor(self, *args):
        """Set or return backgroundcolor of the TurtleScreen.

        Arguments (if given): a color string or three numbers
        in the range 0..colormode or a 3-tuple of such numbers.

        Example (for a TurtleScreen instance named screen):
        >>> screen.bgcolor("orange")
        >>> screen.bgcolor()
        'orange'
        >>> screen.bgcolor(0.5,0,0.5)
        >>> screen.bgcolor()
        '#800080'
        """
        if args:
            color = self._colorstr(args)
        else:
            color = None
        color = self._bgcolor(color)
        if color is not None:
            color = self._color(color)
        return color    

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
        
        shape_svg_id = f'#{shape}'
        _allTurtles.append (self)
          
        self._paths = []
        self._track = []
        self._shape = shape
        self._fill = False
        
        self._screen = _defaultScreen
        self._screen._turtles.append(self)
        #shape_node = document.getElementById(shape)
        #cloned_shape_node = shape_node.cloneNode(True)
        #self._screen.svg.appendChild(cloned_shape_node)

        use_node = document.createElementNS (_ns, 'use')
        """
        <use href="#tree" x="50" y="100" />  
        """
        use_node.setAttribute('href', shape_svg_id)
        #use_node.setAttribute('x', 0 + _offset[0])  # setting this prevents polygon rotation from working
        #use_node.setAttribute('y', 0 + _offset[1])
        
        shape_el = document.getElementById(shape)
        transform = f"translate({0 + _offset[0]},{0 + _offset[1]})"

        if shape_el.tagName == 'polygon':
            use_node.setAttribute('fill', _CFG["fillcolor"])
            use_node.setAttribute('stroke', _CFG["pencolor"])
            use_node.setAttribute('stroke-width', 1)
            use_node.setAttribute('fill-rule', 'evenodd')
            transform += " rotate(-90)" # polygons are drawn pointing top, images pointing right :-/

        use_node.setAttribute('id', f"turtle-{id(self)}")

        use_node.setAttribute('transform', transform)


        self._screen.svg.appendChild(use_node)

        self.reset()
        print(f"{self._heading=}")

    #def _transform(self):
    #TODO

    def reset(self):
        self._heading = 0 # math.pi / 2  # note zero makes the sun example go in the lower left corner..  
        self.pensize(1)
        self.color('black', 'black')
        self.down()
        self._track = []    # Need to make track explicitly because:
        self.home()         # Makes a position but needs a track to put in in
        self.clear()        # Makes a track but needs a position to initialize it with

    def clear (self):
        for path in self._paths:
            _svg.removeChild(path)
        self._paths = []

        self._track = []
        self._moveto(self._position)

    def _flush(self):
        if _debug:
            print('Flush:', self._track)

        if len(self._track) > 1:
            path = document.createElementNS (_ns, 'path')
            path.setAttribute('d', ' '.join (self._track))
            path.setAttribute('stroke', self._pencolor if self._pencolor != None else 'none')
            path.setAttribute('stroke-width', self._pensize)
            path.setAttribute('fill', self._fillcolor if self._fill and self._fillcolor != None else 'none')           
            path.setAttribute('fill-rule', 'evenodd')
            _svg.appendChild(path)
            self._paths.append(path)

            self._track = []
            self._moveto(self._position)   # _track should start with a move command

    def done(self):
        self._flush()

    def pensize(self, width):
        self._flush()
        if width == None:
            return self._pensize
        else:
            self._pensize = width

    def color(self, pencolor, fillcolor = None):
        self._flush()
        self._pencolor = pencolor

        if fillcolor is not None:
            self._fillcolor = fillcolor

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

    def _moveto(self, x, y = None):
        wasdown = self.isdown()
        self.up()
        self.goto(x, y)
        if wasdown:
            self.down()

    def home(self):
        self._moveto(0, 0)

    def position(self):
        return self._position[:]

    def pos(self):
        return self.position()

    def distance(self, x, y = None):
        if y is None:
            other = x
        else:
            other = [x, y]

        dX = other[0] - self._position[0]
        dY = other[1] - self._position[1]

        return math.sqrt (dX * dX + dY * dY)

    def up(self):
        self._down = False

    def down(self):
        self._down = True

    def isdown(self):
        return self._down

    def _predict(self, length):
        delta = [math.sin(self._heading), math.cos(self._heading)]
        return [self._position[0] + length * delta[0], self._position[1] + length * delta[1]]

    def forward(self, length):
        self._position = self._predict(length)

        self._track.append('{} {} {}'.format(
            'L' if self._down else 'M',
            self._position[0] + _offset[0],
            self._position[1] + _offset[1])
        )

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

    def left(self, angle):
        self._heading = (self._heading + math.pi * angle / 180) % (2 * math.pi)

    def right(self, angle): 
        self.left(-angle)

    def begin_fill(self):
        self._flush()
        self._fill = True

    def end_fill(self):
        self._flush()
        self._fill = False

    def speed(speed = None):
        pass

_defaultTurtle = Turtle()
_timer = None

def reset():
    global _timer, _allTurtles
    if _timer:
        clearTimeout(_timer)
    bgcolor('white')
    for turtle in _allTurtles:
        turtle.reset()
        turtle.done()

def clear():
    global _allTurtles
    for turtle in _allTurtles:
        turtle.clear()

def ontimer(fun, t = 0):
    global _timer
    _timer = setTimeout(fun, t)

def done():                            _defaultTurtle.done()
def pensize(width):                    _defaultTurtle.pensize(width)
def color(pencolor, fillcolor = None): _defaultTurtle.color(pencolor, fillcolor)
def home():                            _defaultTurtle.home()
def goto(x, y = None):                 _defaultTurtle.goto(x, y)
def position(): return _defaultTurtle.position()
def pos(): return _defaultTurtle.pos()
def distance(x, y = None): return _defaultTurtle.distance(x, y)
def up():                              _defaultTurtle.up()
def down():                            _defaultTurtle.down()
def forward(length):                   _defaultTurtle.forward(length)
def back(length):                      _defaultTurtle.back(length)
def circle(radius):                    _defaultTurtle.circle(radius)
def left(angle):                       _defaultTurtle.left(angle)
def right(angle):                      _defaultTurtle.right(angle)
def begin_fill():                      _defaultTurtle.begin_fill()
def end_fill():                        _defaultTurtle.end_fill()
def speed(speed):                      _defaultTurtle.speed(speed)
