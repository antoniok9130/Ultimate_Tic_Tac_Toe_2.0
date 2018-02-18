import time

from Game.UTTT import UTTT

g = UTTT()
#g.add_boards(board1d=Board1D(), board2drows=Board2Drows())
start_time = time.time()
g.runSimulation()
elapsed_time = time.time() - start_time
print(elapsed_time)
g.print()

print(g.winner)