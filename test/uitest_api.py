""" API tests

NOTE: pytests can only be run in a browser environment

TODO: usually pytest can run them all, but for some reason
the script appears to never end.

"""


from turtleps import *
import turtleps as tps
import upytest


exc_data = [
    CDTNException,
    CDTNValueError,
    CDTNRuntimeError,
]

def test_exceptions():
    """ TODO check html elements display
    """
    for Exc in exc_data:
        with upytest.raises(Exc) as e_info:
            raise Exc('zam')
        tps._info('!!!!! e_info', e_info)
        tps._info('!!!!! e_info.exception', e_info.exception)
        
        #s = str(e_info.value)    # doesn't work in upytest
        s = str(e_info.exception)  
        

        assert Exc.__name__ in s
        assert 'zam' in s
        
        with upytest.raises(Exc) as e_info:
            raise Exc('gib', 'zv', 'tk')
        
        tps._debug(e_info)

        #s = str(e_info.value)
        s = str(e_info.exception)
        
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

async def test_slide():
    s = Sprite()
    with upytest.raises(CDTNValueError) as e_info:
        await s.slide(5,7,-2)
    tps._debug(e_info)

    s.slide(-5,-7,0)  # equivalent to teletransport
                      # NOTE: fails with upytest
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
    with upytest.raises(CDTNException) as e_info:
        screen.register_shape('c.d.jpg')
    tps._debug(e_info)


async def test_double_init():
    """@since 0.9.0
    """
    tps._ge_loaded = False # TODO better propert reset..

    await ge_init()

    with upytest.raises(CDTNRuntimeError) as e_info:
        await ge_init()
    tps._debug(e_info)



async def test_register_after_init():
    """@since 0.9.0
    """
    tps._ge_loaded = False # TODO better propert reset..

    screen = Screen()    
    screen.register_shape('ab.jpg')
    await ge_init()
    with upytest.raises(CDTNRuntimeError) as e_info:
        screen.register_shape('cd.jpg')
    tps._debug(e_info)


def test_shape_image_ge_not_inited():
    """@since 0.9.0
    """
    tps._ge_loaded = False # TODO better propert reset..

    screen = Screen()    
    screen.register_shape('ab.jpg')
    ada = Sprite()
    with upytest.raises(CDTNRuntimeError) as e_info:
        ada.shape('ab.jpg')
    tps._debug(e_info)

def test_to_foreground_to_background():
    """@since 0.11.0
    """
    screen = Screen()
    screen.clear()
    # raises even if only one sprite
    with upytest.raises(CDTNRuntimeError) as e_info:
        screen.background.to_foreground()

    ada = Sprite(shape="turtle")
    bob = Sprite(shape="square")

    c = screen.svg_sprites.children
    
    assert c[0].id  == screen.background.svg.id
    assert c[1].id  == screen._defaultSprite.svg.id
    assert c[2].id  == ada.svg.id
    assert c[3].id  == bob.svg.id
    
    with upytest.raises(CDTNRuntimeError) as e_info:
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
    
 
