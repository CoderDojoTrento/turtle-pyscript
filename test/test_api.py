
from turtleps import *


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


    