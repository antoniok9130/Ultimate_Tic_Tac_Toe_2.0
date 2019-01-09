from Game.Numba.MCTS_Logic import *
import time

from random import sample
from numba import jit
import numpy as np
# from sklearn.utils.extmath import softmax

from UTTT.Logic import *
from UTTT.utils import *
from .Node import *
from UTTT.second_move import *

def getMove(node, model, device, iterations=100):
    """
    Parameters
    ----------
    model : torch.nn.module
        The DQN model
    device : torch.device
        The device being used to feed forward
    iterations : int, default 3200
        The number of iterations to perform
    """
    move = isNextWin(node)
    if move is not None:
        # time.sleep(1)
        # print("Instant Win!")
        return move

    if node.length == 0:
        return sample(first_move_distribution, 1)[0]

    if node.length == 1:
        # time.sleep(1)
        # print("Instant Win!")
        return get_second_move(node.move[0], node.move[1])

    i = 0
    while (i < iterations):
        select(node, model, device)
        i += 1

    if node.numVisits == 0:
        raise Exception("No Move found...")

    return getChildVisitedMost(node).getMove()


def select(node, model, device):
    if not node.hasChildren():
        node.init()

        if node.winner != N:
            backpropogate(node, 1)
        else:
            expand(node, model, device)

    else:
        select(getChildHighestValue(node), model, device)


def getChildVisitedMost(node):
    index = argmax(np.array([child.numVisits for child in node.children]))
    return node.getChild(index)

def getChildHighestValue(node):
    index = argmax(np.array([child.getValue() for child in node.children]))
    return node.getChild(index)


def expand(node, model, device):
    if not node.hasChildren():
        quadrants = node.buildQuadrant()
        board     = node.buildBoard2D()
        
        legalMoves   = getLegalMovesField(quadrants, board, node.move)
        legalMoves2D = unflatten_legalMoves(legalMoves)

        if len(legalMoves2D) > 0:
            board = np.array(unravel_board(board))
            P, v = model.predict(board, device, preprocess=True)
            np.multiply(P, legalMoves, P)
            v = v[0]
            node.initChildren()

            for legalMove in legalMoves2D:
                node.addChild(node.__class__(P[flatten_move(legalMove)], legalMove, node, False))

            # for child in node.children:
            #     child.incrementAction(0)

            backpropogate(node, v)


def backpropogate(node, actionValue):
    current = node
    while current is not None:
        current.incrementAction(actionValue)
        actionValue *= -1
        current = current.parent


