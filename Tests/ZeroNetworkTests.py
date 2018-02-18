from Game.UTTT import UTTT
from Model.ZeroNetwork import ZeroNetwork

zn = ZeroNetwork()
g = UTTT()
g.runSimulation()
print(zn.feed_forward(g.board))
