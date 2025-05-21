""" Danger forever

Stop test

"""

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("WARNING: Going to work forever and will block UI")
eprint()
eprint("            Stop buttons won't work :-/..")
eprint()
eprint("To stop in Chrome: press Shift-Esc and select 'End process'")

#while True:
#    pass