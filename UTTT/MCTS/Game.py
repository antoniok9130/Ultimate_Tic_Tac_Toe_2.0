from Game.Numba.MCTS_Logic import *
import time

import numpy as np

from ..Logic import *
from .Node import *


def getChildVisitedMost(node):
    mostVisited = 0
    index = -1
    for i, child in enumerate(node.getChildren()):
        if child.getNumVisits() > mostVisited or \
                (child.getNumVisits() == mostVisited and np.random.rand(1) > 0.5):
            mostVisited = child.getNumVisits()
            index = i

    return node.getChild(index)



def getChildHighestUCT(node):
    highestUCT = 0
    index = -1
    for i, child in enumerate(node.getChildren()):
        if child.getUCT() > highestUCT or \
                (child.getUCT() == highestUCT and np.random.rand(1) > 0.5):
            highestUCT = child.getUCT()
            index = i

    return node.getChild(index)


def backpropogate(node: UTTT_Node, winner):

    current = node
    while current is not None:
        current.incrementWins()
        current.incrementVisits()
        current = current.parent
        if current is not None:
            current.incrementVisits()
            current = current.parent


def randomPolicy(move, quadrants, board):
    if move is not None and quadrants[move[1]] == N:
        move[0] = move[1]

    else:
        move[0] = getRandomRemaining(quadrants)

    move[1] = getRandomRemaining(board[move[0]])

    return move


def runSimulation(node):
    winner, length = simulation(node, randomPolicy)
    return winner


def expand(node, simulate=True, runSimulation=runSimulation):
    if not node.hasChildren():
        legalMoves = []
        allQuadrants = np.zeros(9, dtype=int)
        node.buildQuadrant(allQuadrants)

        if node.hasMove() and allQuadrants[node.getLocal()] == N:
            nextQuadrant = np.zeros(9, dtype=int)
            node.buildQuadrant(nextQuadrant, node.getLocal())
            legalMoves = [(node.getLocal(), i) for i, q in enumerate(nextQuadrant) if q == N]

        else:
            board = np.zeros((9, 9))
            node.buildBoard2D(board)
            legalMoves = [(node.getLocal(), i) for i, aQ in enumerate(allQuadrants) if aQ == N 
                                               for j in range(9) if board[i][j] == N]

        if len(legalMoves) > 0:
            node.initChildren()

            for i, legalMove in enumerate(legalMoves):
                node.addChild(node.__class__(legalMove, node, False))

            if simulate:
                random = node.getChild(np.random.choice(len(node.getChildren()), size=1)[0])
                backpropogate(random, runSimulation(random))


def select(node, select=select, runSimulation=runSimulation):
    if not node.hasChildren():
        node.init()

        if node.getWinner() != N:
            backpropogate(node, node.getWinner())

        elif node.hasMove() and node.getNumVisits() == 0:
            backpropogate(node, runSimulation(node))

        else:
            expand(node, runSimulation=runSimulation)

    else:
        select(getChildHighestUCT(node), select=select, runSimulation=runSimulation)



def getMove(node, iterations=3200, select=select, runSimulation=runSimulation):
    move = isNextWin(node)
    if move is not None:
        time.sleep(1)
        print("Instant Win!")
        return move

    i = 0
    while (i < iterations):
        select(node, select=select, runSimulation=runSimulation)
        i += 1

    if node.getNumVisits() == 0:
        raise Exception("No Move found...")

    print("Search Space Size:  {0}".format(node.getNumVisits()))
    return getChildVisitedMost(node).getMove()


