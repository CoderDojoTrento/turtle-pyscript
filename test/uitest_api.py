
from turtleps import *
import turtleps as tps
import pytest_asyncio
import pytest

"""
This works in a browser environment, but sadly not in a regular desktop console one.
 
"""

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
    
    screen = Screen()
    screen.register_shape('c d.jpg')
    with pytest.raises(CDTNException) as e_info:
        screen.register_shape('c.d.jpg')
        tps._debug(e_info)

pytest.main(["--asyncio-mode=auto", 
             "-W","ignore",     # crude but at least I don't see pytest-asyncio warning below 
            "uitest_api.py"])
 


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
 
