from MCTS_Logic import *
import time

import numpy as np

from MCTS_Logic import *
from MCTS_Node import *

def getMove(node, thinkingTime = 5):
    AIPlayer = P2 if node.getPlayer() == P1 else P1
    quadrants = np.zeros(9, dtype=int)
    node.buildQuadrant(quadrants)
    if node.getNextQuadrant() != -1:
        if potential3inRow(quadrants, node.getNextQuadrant(), AIPlayer):
            quadrant = np.zeros(9, dtype=int)
            node.buildQuadrant(quadrant, node.getNextQuadrant())
            for i, q in enumerate(quadrant):
                if q == N and potential3inRow(quadrant, i, AIPlayer):
                    time.sleep(1)
                    print("Instant Win!")
                    return [node.getNextQuadrant(), i]

    else:
        for i, q in enumerate(quadrants):
            if q == N and potential3inRow(quadrants, i, AIPlayer):
                quadrant = np.zeros(9, dtype=int)
                node.buildQuadrant(quadrant, i)
                for j, q1 in enumerate(quadrant):
                    if q1 == N and potential3inRow(quadrant, j, AIPlayer):
                        time.sleep(1)
                        print("Instant Win!")
                        return [i, j]


    # thinkingTime *= 1000
    end = time.time()+thinkingTime

    print("{0} + {1} = {2}".format(time.time(), thinkingTime, end))
    while (time.time() < end):
        select(node)
        select(node)
        select(node)
        select(node)
        select(node)

    if node.getNumVisits() == 0:
        raise Exception("No Move found...")

    print("Search Space Size:  {0}".format(node.getNumVisits()))
    return getChildVisitedMost(node).getMove()


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


def select(node):
    if not node.hasChildren():
        node.init()

        if node.getWinner() != N:
            backpropogate(node, node.getWinner())

        elif node.hasMove() and node.getNumVisits() == 0:
            backpropogate(node, runSimulation(node))

        else:
            expand(node)

    else:
        select(getChildHighestUCT(node))



def expand(node):
    if not node.hasChildren():
        numChildren = 0
        legalMoves = []
        allQuadrants = np.zeros(9, dtype=int)
        node.buildQuadrant(allQuadrants)

        if node.hasMove() and allQuadrants[node.getLocal()] == N:
            nextQuadrant = np.zeros(9, dtype=int)
            node.buildQuadrant(nextQuadrant, node.getLocal())
            for i, q in enumerate(nextQuadrant):
                if q == N:
                    legalMoves.append((node.getLocal(), i))

        else:
            board = np.zeros((9, 9))
            node.buildBoard2D(board)
            for i, aQ in enumerate(allQuadrants):
                if aQ == N:
                    for j in range(9):
                        if board[i][j] == 0:
                            legalMoves.append([i, j])

        if len(legalMoves) > 0:
            node.initChildren()

            for i, legalMove in enumerate(legalMoves):
                node.addChild(MCTS_Node(legalMove, node, False))

            random = node.getChild(np.random.choice(len(node.getChildren()), size=1)[0])
            backpropogate(random, runSimulation(random))



def runSimulation(node):
    node.init()
    board = np.zeros((9, 9))
    node.buildBoard2D(board)
    quadrants = np.zeros(9, dtype=int)
    node.buildQuadrant(quadrants)

    cdef int numRemainingQuadrants = 0
    numRemainingBoard = np.zeros(9, dtype=int)
    potentialQuadrants = np.zeros(9, dtype=int)

    for i, quadrant in enumerate(quadrants):
        if quadrant == N:
            numRemainingQuadrants += 1
            potentialQuadrants[i] = potential3inRow(quadrants, i)
            for j in range(9):
                if board[i][j] == N:
                    numRemainingBoard[i] += 1

    move = node.getMove()
    if move is None:
        move = [-1, -1]

    player = node.getPlayer()
    winner = node.getWinner()

    while winner == N:
        if move[1] != -1 and quadrants[move[1]] == N:
            move[0] = move[1]

        else:
            move[0] = getRandomRemaining(quadrants)

        if potentialQuadrants[move[0]] == player or potentialQuadrants[move[0]] == B:
            for i in range(9):
                if board[move[0]][i] == N and potential3inRow(board[move[0]], i, player):
                    return player

        move[1] = getRandomRemaining(board[move[0]])
        player = P1 if player == P2 else P2
        board[move[0]][move[1]] = player
        numRemainingBoard[move[0]] -= 1

        if check3InRow(board[move[0]], move[1]):
            quadrants[move[0]] = player
            numRemainingQuadrants -= 1

            updatePotential3inRow(potentialQuadrants, quadrants, move[0])

            if check3InRow(quadrants, move[0]):
                winner = player
                return player

            elif numRemainingQuadrants <= 0:
                winner = T
                return T

        elif numRemainingBoard[move[0]] <= 0:
            quadrants[move[0]] = T
            numRemainingQuadrants -= 1

            if numRemainingQuadrants <= 0:
                winner = T
                return T

    return winner






def backpropogate(node, winner):
    if node.getPlayer() == winner:
        node.incrementWins()

    node.incrementVisits()

    if node.getParent() is not None:
        backpropogate(node.getParent(), winner)

    node.updateUCT()
