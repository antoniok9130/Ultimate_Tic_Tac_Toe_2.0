
import time
import sys

current_time_milli = lambda: int(round(time.time() * 1000))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)