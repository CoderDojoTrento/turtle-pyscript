
from turtleps import *
import turtleps
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


def test_sanitize_id():

    sid = turtleps._sanitize_id

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


pytest.main(["uitest_api.py"])
    