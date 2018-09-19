from random import randint

import numpy as np
from UTTT_Logic import *

# @jit(nopython=True, cache=True)
def getRandomRemaining(quadrant):
    r = randint(0, 8)
    while (quadrant[r] != N):
        r = randint(0, 8)

    if quadrant[r] == N:
        return r

    print("Could not find Random Remaining for: ", quadrant)
    print(quadrant[0] == N)
    raise Exception("")


# @jit(cache=True)
def generateGame():

    board = np.zeros((9, 9), dtype=int)
    quadrants = np.zeros(9, dtype=int)

    numRemainingQuadrants = 9
    numRemainingBoard = np.full(9, 9, dtype=int)
    potentialQuadrants = np.full(9, 9, dtype=int)

    g = -1 # global square
    l = -1 # local square

    moves = []

    player = 1
    winner = N

    while winner == N:
        if l != -1 and quadrants[l] == N:
            g = l

        else:
            g = getRandomRemaining(quadrants)

        if potentialQuadrants[g] == player or potentialQuadrants[g] == B:
            for i in range(9):
                if board[g][i] == N and potential3inRow(board[g], i, player):
                    return player

        l = getRandomRemaining(board[g])
        player = P1 if player == P2 else P2
        board[g][l] = player
        moves.append((g, l))
        numRemainingBoard[g] -= 1

        if check3InRowAt(board[g], l):
            quadrants[g] = player
            numRemainingQuadrants -= 1

            updatePotential3inRow(potentialQuadrants, quadrants, g)

            if check3InRowAt(quadrants, g):
                winner = player

            elif numRemainingQuadrants <= 0:
                winner = T

        elif numRemainingBoard[g] <= 0:
            quadrants[g] = T
            numRemainingQuadrants -= 1

            if numRemainingQuadrants <= 0:
                winner = T

    return moves

# @jit(nopython=True, cache=True)
def generateGames():
    games = []
    array = np.zeros(180) # 81+9+81+9
