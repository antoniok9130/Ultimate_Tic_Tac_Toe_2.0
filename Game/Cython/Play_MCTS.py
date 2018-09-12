from MCTS_Game import getMove
from MCTS_Node import *

node = MCTS_Node()
node.setChild([4, 4])
node = node.getChild(0)
move = getMove(node)

print("{0} found in {1} iterations".format(move, node.getNumVisits()))