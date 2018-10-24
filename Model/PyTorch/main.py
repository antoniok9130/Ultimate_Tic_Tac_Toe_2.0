
import sys
sys.path.append("../../Game/Python")

from UTTT_Logic import *
from NN_MCTS_Node import NN_MCTS_Node as Node
from NN_MCTS import NN_MCTS as MCTS, board_to_input
from Model import UTTT_Model
from random import shuffle, randint

import time
import torch
import numpy as np

current_time_milli = lambda: int(round(time.time() * 1000))


model = UTTT_Model("./ModelInstances/uttt_conv1_model_87")

mcts = MCTS(model, model)

board = np.zeros((9, 9))
quadrants = np.zeros(9)

node = Node()

i = 0
while node.getWinner() == N:
    printBoard(board, quadrants)

    move = tuple(input("Enter Move:  ").replace(" ", ""))
    if len(move) > 1:
        g = int(move[0])
        l = int(move[1])
    elif node.getLocal() != -1 and node.getNextQuadrant() != -1 and len(move) > 0:
        g = node.getLocal()
        l = int(move[0])
    else:
        print("You must enter a quadrant")
        continue

    if node.isLegal((g, l)):
        node.setChild([g, l])
        node = node.getChild(0)

        board[g][l] = node.getPlayer()
        if node.getCapturedQuadrant() != -1:
            quadrants[node.getCapturedQuadrant()] = node.getPlayer()

        printBoard(board, quadrants)
        if node.getWinner() == N:
            start = current_time_milli()
            g, l = mcts.getMove(node)
            end = current_time_milli()
            node.setChild([g, l])
            node = node.getChild(0)

            board[g][l] = node.getPlayer()
            if node.getCapturedQuadrant() != -1:
                quadrants[node.getCapturedQuadrant()] = node.getPlayer()

            print(f"Took {(end-start)/1000.0} seconds to get move:   {g} {l}")
            print(f"Num Iterations:   ", node.getParent().getNumVisits())
            print(f"Confidence:       ", node.getNumWins()/node.getNumVisits())
            print()
    else:
        print(f"{g} {l} is not a legal move")
    

print(f"Player {node.getWinner()} is the winner!")
