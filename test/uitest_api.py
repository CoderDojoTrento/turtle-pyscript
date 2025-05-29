""" API tests

NOTE: pytests can only be run in a browser environment

TODO: usually pytest can run them all, but for some reason
the script appears to never end.

"""


from turtleps import *
import turtleps as tps
import pytest_asyncio
import pytest



exc_data = [
    CDTNException,
    CDTNValueError,
    CDTNRuntimeError,
]

@pytest.mark.parametrize("Exc", exc_data)
def test_exceptions(Exc):
    """ TODO check html elements display
    """

    with pytest.raises(Exc) as e_info:
        raise Exc('zam')
    tps._debug(e_info)
    s = str(e_info.value)

    assert Exc.__name__ in s
    assert 'zam' in s
    
    with pytest.raises(Exc) as e_info:
        raise Exc('gib', 'zv', 'tk')
    
    tps._debug(e_info)

    s = str(e_info.value)
    assert Exc.__name__ in s
    assert 'gib' in s
    assert 'zv' in s    
    assert 'tk' in s

    
def test_xy():
    s = Sprite()
    assert s.x == 0
    assert s.y == 0

    s.x = 5
    assert s.x == 5
    assert s.y == 0


    s.y = 3
    assert s.x == 5
    assert s.y == 3

    s.x += 4
    assert s.x == 9
    assert s.y == 3

    s.y += 7
    assert s.x == 9
    assert s.y == 10

#@pytest.mark.asyncio(loop_scope="session")
async def test_slide():
    s = Sprite()
    with pytest.raises(CDTNValueError) as e_info:
        await s.slide(5,7,-2)
    tps._debug(e_info)

    s.slide(-5,-7,0)  # equivalent to teletransport
    assert s.x == -5
    assert s.y == -7
    

def test_sanitize_id():

    sid = tps._sanitize_id

    assert sid('012') == '012'
    assert sid('a') == 'a'
    assert sid('ab') == 'ab'
    assert sid(r"a.b") == "a-b"
    assert sid(r"你") == r"你"
    assert sid(r"ò") == r"ò"

    assert sid(r"http://") == "http---"
    assert sid(r"c d  e") == "c-d--e"
    assert sid(r"%20") == "-20"
    assert sid("\\") == "-"
    

    assert sid(r"http://basta你rd.còm/bad%20b'ad evi-l__.jpg") == r"http---basta你rd-còm-bad-20b-ad-evi-l__-jpg"

def test_register_id():
    """
    TODO find way to properly reset Screen within same test
    """
    screen = Screen()
    screen.register_shape('a b.jpg')
    el = screen.svg.getElementById("a-b-jpg")
    assert el is not None

def test_register_same_sanitized_id():
    """
    TODO find way to properly reset Screen within same test
    """
    tps._ge_loaded = False # TODO better propert reset..

    screen = Screen()
    screen.register_shape('c d.jpg')
    with pytest.raises(CDTNException) as e_info:
        screen.register_shape('c.d.jpg')
    tps._debug(e_info)


async def test_double_init():
    """@since 0.9.0
    """
    tps._ge_loaded = False # TODO better propert reset..

    await ge_init()

    with pytest.raises(CDTNRuntimeError) as e_info:
        await ge_init()
    tps._debug(e_info)



async def test_register_after_init():
    """@since 0.9.0
    """
    tps._ge_loaded = False # TODO better propert reset..

    screen = Screen()    
    screen.register_shape('ab.jpg')
    await ge_init()
    with pytest.raises(CDTNRuntimeError) as e_info:
        screen.register_shape('cd.jpg')
    tps._debug(e_info)


def test_shape_image_ge_not_inited():
    """@since 0.9.0
    """

    screen = Screen()    
    screen.register_shape('ab.jpg')
    ada = Sprite()
    with pytest.raises(CDTNRuntimeError) as e_info:
        ada.shape('ab.jpg')
    tps._debug(e_info)

def test_to_foreground_to_background():
    """@since 0.11.0
    """
    screen = Screen()
    screen.clear()
    # raises even if only one sprite
    with pytest.raises(CDTNRuntimeError) as e_info:
        screen.background.to_foreground()

    ada = Sprite(shape="turtle")
    bob = Sprite(shape="square")

    c = screen.svg_sprites.children
    
    assert c[0].id  == screen.background.svg.id
    assert c[1].id  == screen._defaultSprite.svg.id
    assert c[2].id  == ada.svg.id
    assert c[3].id  == bob.svg.id
    
    with pytest.raises(CDTNRuntimeError) as e_info:
        screen.background.to_foreground()

    ada.to_foreground()
    assert c[0].id  == screen.background.svg.id
    assert c[1].id  == screen._defaultSprite.svg.id
    assert c[2].id  == bob.svg.id
    assert c[3].id  == ada.svg.id

    ada.to_background()
    assert c[0].id  == screen.background.svg.id
    assert c[1].id  == ada.svg.id
    assert c[2].id  == screen._defaultSprite.svg.id
    assert c[3].id  == bob.svg.id
    
    # this just issues a warning
    screen.background.to_background()
    

res = pytest.main(["--asyncio-mode=auto", 
             "-W","ignore",     # crude but at least I don't see pytest-asyncio warning below 
             "uitest_api.py"])
if res:
    tps._error("******   TEST(S) FAILED!   ******")


"""
uitest_api.py::test_slide
_io.js:15   /lib/python3.12/site-packages/pytest_asyncio/plugin.py:814: DeprecationWarning: pytest-asyncio detected an unclosed event loop when tearing down the event_loop
_io.js:15   fixture: <pyodide.webloop.WebLoop object at 0x14e39a0>
_io.js:15   pytest-asyncio will close the event loop for you, but future versions of the
_io.js:15   library will no longer do so. In order to ensure compatibility with future
_io.js:15   versions, please make sure that:
_io.js:15       1. Any custom "event_loop" fixture properly closes the loop after yielding it
_io.js:15       2. The scopes of your custom "event_loop" fixtures do not overlap
_io.js:15       3. Your code does not modify the event loop in async fixtures or tests
_io.js:15   
_io.js:15     warnings.warn(
"""

 
