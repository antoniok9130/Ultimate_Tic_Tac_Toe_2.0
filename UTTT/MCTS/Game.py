from Game.Numba.MCTS_Logic import *
import time

from numba import jit
import numpy as np

from ..Logic import *
from .Node import *
from ..second_move import *

@jit(cache=True, nopython=True)
def randomPolicy(move, quadrants, board, length):
    if move is not None and quadrants[move[1]] == N:
        g = move[1]
    else:
        g = getRandomRemaining(quadrants)

    move[0] = g
    move[1] = getRandomRemaining(board[g])


@jit(cache=True) # , nopython=True
def randomSimulation(quadrants, board, winner, move, player, length):
    return simulation(quadrants, board, winner, move, player, length, randomPolicy)[0] # winner



def getMove(node, iterations=3200, simulation=randomSimulation):
    """
    Parameters
    ----------
    iterations : int, default 3200
        The number of iterations to perform
    simulation : function
        a Numba JIT-compiled function satisfying the following:

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
    """
    move = isNextWin(node)
    if move is not None:
        # time.sleep(1)
        # print("Instant Win!")
        return move

    if node.length == 1:
        # time.sleep(1)
        # print("Instant Win!")
        return get_second_move(node.move[0], node.move[1])

    i = 0
    while (i < iterations):
        select(node, simulation=simulation)
        i += 1

    if node.getNumVisits() == 0:
        raise Exception("No Move found...")

    return getChildVisitedMost(node).getMove()


def select(node, simulation=randomSimulation):
    if not node.hasChildren():
        node.init()

        if node.winner != N:
            backpropogate(node, node.winner)

        elif node.hasMove() and node.getNumVisits() == 0:
            quadrants = node.buildQuadrant()
            board     = node.buildBoard2D()
            backpropogate(node, simulation(quadrants, board, node.winner, node.move, node.getPlayer(), node.length))

        else:
            expand(node, simulation=simulation)

    else:
        select(getChildHighestUCT(node), simulation=simulation)


def getChildVisitedMost(node):
    mostVisited = 0
    index = -1
    for i, child in enumerate(node.children):
        if child.getNumVisits() > mostVisited or \
                (child.getNumVisits() == mostVisited and np.random.rand(1) > 0.5):
            mostVisited = child.getNumVisits()
            index = i

    return node.getChild(index)


def getChildHighestUCT(node):
    highestUCT = 0
    index = -1
    for i, child in enumerate(node.children):
        if child.getUCT() > highestUCT or \
                (child.getUCT() == highestUCT and np.random.rand(1) > 0.5):
            highestUCT = child.getUCT()
            index = i

    return node.getChild(index)


def expand(node, simulate=True, simulation=randomSimulation):
    if not node.hasChildren():
        quadrants = node.buildQuadrant()
        board     = node.buildBoard2D()
        
        legalMoves = getLegalMoves2D(quadrants, board, node.move)

        if len(legalMoves) > 0:
            node.initChildren()

            for i, legalMove in enumerate(legalMoves):
                node.addChild(node.__class__(legalMove, node, False))

            if simulate:
                random = node.getChild(np.random.randint(len(node.children)))
                backpropogate(random, simulation(quadrants, board, node.winner, node.move, node.getPlayer(), node.length))


def backpropogate(node: UTTT_Node, winner):

    current = node
    if winner == T:
        while current is not None:
            current.incrementVisits()
            current = current.parent

    elif current.getPlayer() == winner:
        while current is not None:
            current.incrementWins()
            current.incrementVisits()
            current = current.parent
            if current is not None:
                current.incrementVisits()
                current = current.parent

    else:
        while current is not None:
            current.incrementVisits()
            current = current.parent
            if current is not None:
                current.incrementWins()
                current.incrementVisits()
                current = current.parent


