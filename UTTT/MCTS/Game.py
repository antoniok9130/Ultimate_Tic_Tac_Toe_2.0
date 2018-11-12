from Game.Numba.MCTS_Logic import *
import time

from numba import jit
import numpy as np

from ..Logic import *
from .Node import *

@jit(cache=True, nopython=True)
def randomPolicy(previousMove, quadrants, board):
    if previousMove is not None and quadrants[previousMove[1]] == N:
        g = previousMove[1]
    else:
        g = getRandomRemaining(quadrants)

    l = getRandomRemaining(board[g])

    return g, l


@jit(cache=True, nopython=True)
def randomSimulation(quadrants, board, winner, move, player):
    return simulation(quadrants, board, winner, move, player, randomPolicy)[0] # winner


def getMove(node, iterations=3200, simulation=randomSimulation):
    move = isNextWin(node)
    if move is not None:
        time.sleep(1)
        print("Instant Win!")
        return move

    i = 0
    while (i < iterations):
        select(node, simulation=simulation)
        i += 1

    if node.getNumVisits() == 0:
        raise Exception("No Move found...")

    print("Search Space Size:  {0}".format(node.getNumVisits()))
    return getChildVisitedMost(node).getMove()


def select(node, simulation=randomSimulation):
    if not node.hasChildren():
        node.init()

        if node.winner != N:
            backpropogate(node, node.winner)

        elif node.hasMove() and node.getNumVisits() == 0:
            quadrants = node.buildQuadrant()
            board     = node.buildBoard2D()
            backpropogate(node, simulation(quadrants, board, node.winner, node.move, node.getPlayer()))

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
        legalMoves = []
        allQuadrants = node.buildQuadrant()

        if node.hasMove() and allQuadrants[node.getLocal()] == N:
            nextQuadrant = node.buildQuadrant(node.getLocal())
            legalMoves = [(node.getLocal(), i) for i, q in enumerate(nextQuadrant) if q == N]

        else:
            board = node.buildBoard2D()
            legalMoves = [(node.getLocal(), i) for i, aQ in enumerate(allQuadrants) if aQ == N 
                                               for j in range(9) if board[i][j] == N]

        if len(legalMoves) > 0:
            node.initChildren()

            for i, legalMove in enumerate(legalMoves):
                node.addChild(node.__class__(legalMove, node, False))

            if simulate:
                random = node.getChild(np.random.randint(len(node.children)))
                quadrants = node.buildQuadrant()
                board     = node.buildBoard2D()
                backpropogate(random, simulation(quadrants, board, node.winner, node.move, node.getPlayer()))


def backpropogate(node: UTTT_Node, winner):

    current = node
    while current is not None:
        current.incrementWins()
        current.incrementVisits()
        current = current.parent
        if current is not None:
            current.incrementVisits()
            current = current.parent


