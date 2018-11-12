from Game.Numba.MCTS_Logic import *
import time

from numba import jit
import numpy as np

from ..Logic import *
from .Node import *

@jit(cache=True, nopython=True)
def randomPolicy(move, quadrants, board):
    if move is not None and quadrants[move[1]] == N:
        g = move[1]
    else:
        g = getRandomRemaining(quadrants)

    move[0] = g
    move[1] = getRandomRemaining(board[g])


@jit(cache=True, nopython=True)
def randomSimulation(quadrants, board, winner, move, player):
    return simulation(quadrants, board, winner, move, player, randomPolicy)[0] # winner



def play_MCTS(iterations=3200, simulation=randomSimulation):
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
        move = getMove(node, iterations=iterations, simulation=simulation)
        end = current_time_milli()
        print("Search Space Size:  {0}".format(node.getNumVisits()))
        node.setChild(move)
        node = node.getChild(0)
        print(f"g:   {move[0]}      l:   {move[1]}")
        print(f"w:   {node.numWins}      v:   {node.numVisits}")
        print(f"confidence:   {node.getConfidence()}")
        print(f"time:         {(end-start)/1000.0} seconds")

    print(f"{node.winner} is the winner!")



def getMove(node, iterations=3200, simulation=randomSimulation):

    move = isNextWin(node)
    if move is not None:
        # time.sleep(1)
        # print("Instant Win!")
        return move

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
        quadrants = node.buildQuadrant()
        board     = node.buildBoard2D()
        
        legalMoves = getLegalMoves2D(quadrants, board, node.move)

        if len(legalMoves) > 0:
            node.initChildren()

            for i, legalMove in enumerate(legalMoves):
                node.addChild(node.__class__(legalMove, node, False))

            if simulate:
                random = node.getChild(np.random.randint(len(node.children)))
                backpropogate(random, simulation(quadrants, board, node.winner, node.move, node.getPlayer()))


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


