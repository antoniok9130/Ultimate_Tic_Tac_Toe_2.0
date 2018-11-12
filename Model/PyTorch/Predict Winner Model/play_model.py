
import sys
sys.path.append("..\\..\\..\\")

from numba import jit
import numpy as np

from UTTT import *
from Predict_Model import *

model = Predict_Model("../ModelInstances/predict1/predict1_model_epoch_35")

@jit(cache=True) # , nopython=True)
def modelSimulation(quadrants, board, winner, move, player):
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

    prediction = model.predict(extract_features(quadrants, board))
    winner = prediction.argmax()
    if winner == 0:
        return T, 0
    if winner == 1:
        return P1, 0
    if winner == 2:
        return P2, 0
        

play_MCTS(iterations=3200, simulation=modelSimulation)





