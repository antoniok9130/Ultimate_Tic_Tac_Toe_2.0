
import sys
sys.path.append("..\\..\\..\\")
import subprocess as sp

import numpy as np
import torch

from UTTT import *
from random import shuffle, randint, choice
from Policy_Model import *



# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# print("Training on:  ", device)

# policy_name = "../ModelInstances/policy2/policy2_model"
model = Policy_Model(exploreProb = 0.05) # state_dict_path=policy_name,   .to(device)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.005, momentum=0.9)


@jit
def modelPolicy(move, quadrants, board):
    legalMoves = getLegalMoves1D(quadrants, board, move)

    probs = model.predict(extract_features(quadrants, board))

    best_moves = []
    highest_prob = -1
    for legalMove in legalMoves:
        if probs[legalMove] > highest_prob:
            best_moves = [legalMove]
        elif probs[legalMove] == highest_prob:
            best_moves.append(legalMove)

    best_move = best_moves[np.random.randint(len(best_moves))]
    return [int(best_move//9), best_move%9]


@jit(cache=True)
def modelSimulation(quadrants, board, winner, move, player):
    
    if winner != N:
        return winner, 0
    
    if move is not None and quadrants[move[1]] == N:
        if potential3inRow_wp(quadrants, move[1], player):
            return player, 1 # next move
    else:
        for g in range(9):
            if quadrants[g] == N and potential3inRow_wp(quadrants, g, player):
                return player, 1 # next move

    return simulation_p(quadrants, board, winner, move, player, modelPolicy)[0]



play_MCTS(iterations=1600, simulation=modelSimulation)
