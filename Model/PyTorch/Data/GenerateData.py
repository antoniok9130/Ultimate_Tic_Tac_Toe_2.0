import time

from GameGenerator import *

current_time_milli = lambda: int(round(time.time() * 1000))

start = current_time_milli()

for _ in range(10000):
    game = generateGame()

print(current_time_milli() - start)