
import upytest
import sys

res = await upytest.run("./uitest_api")


if res['fails']:
    print("ERROR:", "******   TEST(S) FAILED!   ******", file=sys.stderr, )
    

# ------ OLD PYTEST STUFF, WAS IN test/uitest_api.py

"""
res = pytest.main(["--asyncio-mode=auto", 
             "-W","ignore",     # crude but at least I don't see pytest-asyncio warning below 
             "uitest_api.py"])
"""

#if res:
#    tps._error("******   TEST(S) FAILED!   ******")


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


