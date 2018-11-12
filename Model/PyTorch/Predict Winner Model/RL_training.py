
import sys
sys.path.append("..\\..\\..\\")

from numba import jit
import numpy as np

from UTTT import *
from Predict_Model import *

model = Predict_Model("../ModelInstances/predict1/predict1_model_epoch_35")

@jit
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
    
    if move is not None and quadrants[move[1]] == N:
        if potential3inRow_wp(quadrants, move[1], player):
            return player, 1 # next move
    else:
        for g in range(9):
            if quadrants[g] == N and potential3inRow_wp(quadrants, g, player):
                return player, 1 # next move

    prediction = model.predict(extract_features(quadrants, board))
    winner = prediction.argmax()
    # print(prediction)
    if winner == 0:
        return T, 2 # at least two into the future
    if winner == 1:
        return P1, 2 # at least two into the future
    if winner == 2:
        return P2, 2 # at least two into the future
        

node = MCTS_Node()

    while node.winner == N:
        print()
        printBoard(node.buildBoard2D(), node.buildQuadrant())
        move = [int(m) for m in list(input("Enter Move:  ").replace(" ", ""))]
        if len(move) == 1:
            if node.move is not None:
                move = [node.move[1], move[0]]
            else:
                print("Invalid Move:  Need to enter quadrant then move")
                continue

        elif len(move) != 2:
            print("Invalid Move:  ", move)
            continue

        
        if not node.isLegal(move):
            print("Illegal Move:  ", move)
            continue

        node.setChild(move)
        node = node.getChild(0)

        printBoard(node.buildBoard2D(), node.buildQuadrant())

        print("Computer is thinking...")
        start = current_time_milli()
        move = getMove(node, iterations=iterations, simulation=modelSimulation)
        end = current_time_milli()
        node.setChild(move)
        node = node.getChild(0)
        print(f"g:   {move[0]}      l:   {move[1]}")
        print(f"w:   {node.numWins}      v:   {node.numVisits}")
        print(f"confidence:   {node.getConfidence()}")
        print(f"time:         {(end-start)/1000.0} seconds")

    print(f"{node.winner} is the winner!")





