import numpy as np
from numba import jit
import numba

from .Logic import *

class UTTT_Node:

    
    def __init__(self, move = None, parent = None, initialize = False):
        self.winner = N
        # self.player = N
        self.nextQuadrant = -1
        self.capturedQuadrant = N
        self.length = 0

        self.move = move
        self.parent = parent
        self.children = None

        self.initialized = False
        self.moveSet = False

        if parent is None:
            # self.player = N
            self.length = 0
            self.initialized = True

        else:
            self.winner = parent.winner
            # self.player = P2 if parent.player == P1 else P1
            self.length = parent.length+1

            if move is not None and not self.capturedQuadrantEquals(move[1], True):
                self.nextQuadrant = move[1]

            if initialize:
                if self.winner == N:
                    self.init()
                else:
                    initialized = True

    
    def init(self):
        if not self.initialized:
            if self.move is not None:
                self.setMove()

            self.initialized = True


    
    def setMove(self, move = None):
        if move is not None and self.move is None:
            self.move = move

        if not self.moveSet and self.move is not None:
            currentQuadrant = self.buildQuadrant(quadrant=self.move[0])
            self.capturedQuadrant = check3InRow(currentQuadrant)

            if self.capturedQuadrant != N:
                allQuadrants = self.buildQuadrant()
                self.winner = check3InRow(allQuadrants)

            self.moveSet = True


    
    def isLegal(self, move):
        return (self.nextQuadrant == -1 or move[0] == self.nextQuadrant) and \
                not self.moveOrCapturedQuadrantEquals(move, move[0])


    
    def moveEquals(self, move):
        return self.move is not None and self.move[0] == move[0] and self.move[1] == move[1]


    
    def capturedQuadrantEquals(self, quadrant, backpropogate = False):
        return (self.capturedQuadrant != N and self.move is not None and self.move[0] == quadrant) or \
               (backpropogate and self.parent is not None and self.parent.capturedQuadrantEquals(quadrant, backpropogate))


    
    def moveOrCapturedQuadrantEquals(self, move, quadrant):
        return self.moveEquals(move) or self.capturedQuadrantEquals(quadrant) or \
               (self.parent is not None and self.parent.moveOrCapturedQuadrantEquals(move, quadrant))


    
    def hasMove(self):
        return self.move is not None

    
    def getMove(self):
        return None if self.move is None else [self.move[0], self.move[1]]

    
    def getGlobal(self):
        return self.move[0] if self.move is not None else None

    
    def getLocal(self):
        return self.move[1] if self.move is not None else None

    
    # def getWinner(self):
    #     return self.winner

    
    # def getNextQuadrant(self):
    #     return self.nextQuadrant

    # def getCapturedQuadrant(self):
    #     return self.capturedQuadrant


    def __len__(self):
        return self.length

    def getPlayer(self):
        return 2-(self.length%2)

    def getParent(self):
        return self.parent

    def hasChildren(self):
        return self.children is not None

    # def getChildren(self):
    #     return self.children

    def initChildren(self):
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getChild(self, index):
        return self.children[index]

    def setChild(self, move):
        if self.children is not None:
            for child in self.children:
                if child.move[0] == move[0] and child.move[1] == move[1]:
                    self.children = [child]
                    return

        if self.isLegal(move):
            self.children = [self.__class__(move, self, True)]

        else:
            print("Could not find child with move:  {0} {1}".format(move[0], move[1]))
            exit(1)


    
    def buildQuadrant(self, quadrant = None):
        array = np.zeros(9, dtype=np.intc)

        current = self
        if quadrant is None:
            while current is not None:
                if current.capturedQuadrant != N:
                    array[current.move[0]] = current.capturedQuadrant

                current = current.parent

        else:
            while current is not None:
                if current.move is not None and current.move[0] == quadrant:
                    array[current.move[1]] = 2-(current.length%2)

                current = current.parent

        return array


    def buildBoard2D(self):
        array = np.zeros((9, 9), dtype=np.intc)

        current = self
        while current is not None:
            if current.move is not None:
                array[current.move[0]][current.move[1]] = 2-(current.length%2)

            current = current.parent

        return array


# if __name__ == "__main__":
#     print(numba.typeof(UTTT_Node))
