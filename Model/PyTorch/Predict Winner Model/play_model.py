
import sys
sys.path.append("..\\..\\..\\")

from numba import jit
import numpy as np

from UTTT import *
from Predict_Model import *

model = Predict_Model("../ModelInstances/predict8/predict_model_min_average_loss")

@jit
def modelSimulation(quadrants, board, winner, move, player, length):
    '''
    Parameters
    ----------
    quadrants : 1d list
        a list of length nine representing the current quadrant state
    board : 2d list
        a 2d list of length nine by nine representing the current board state
    winner : int
        the winner if any
    move : 1d list
        a list of length two containing the quadrant and square of the previous move
    player : int
        the current player

    Returns
    ----------
    winner : int
        an int signifying the predicted winner
    length : int
        how far into the future the win occured
    '''
    
    if winner != N:
        return winner, 0
    
    if move is not None and quadrants[move[1]] == N:
        if potential3inRow_wp(quadrants, move[1], player):
            return player, 1 # next move
    else:
        for g in range(9):
            if quadrants[g] == N and potential3inRow_wp(quadrants, g, player):
                return player, 1 # next move

    prediction = model.predict(extract_features(quadrants, board), length)
    winner = prediction.argmax()
    # print(prediction)
    if winner == 0:
        return T, 2 # at least two into the future
    if winner == 1:
        return P1, 2 # at least two into the future
    if winner == 2:
        return P2, 2 # at least two into the future
        
def getModelMove(node):
    return getAIMove(node, verbose=True, iterations=4800, simulation=modelSimulation)

play_UTTT(P2_move=getModelMove)





