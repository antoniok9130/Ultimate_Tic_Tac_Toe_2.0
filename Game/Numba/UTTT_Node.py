from numba import jitclass, int32

from Game.Numba.UTTT_Logic import *

spec = [
    ("winner", int32),
    ("player", int32),
    ("nextQuadrant", int32),
    ("capturedQuadrant", int32),
    ("length", int32),

    ("move", int32[:])
]

@jitclass(spec)
class UTTT_Node:

    
    def __init__(self, move = None, parent = None, initialize = False):
        self.winner = N
        self.player = N
        self.nextQuadrant = -1
        self.capturedQuadrant = N
        self.length = 0

        self.move = move
        self.parent = parent
        self.children = None

        self.initialized = False
        self.moveSet = False

        if parent is None:
            self.player = P1
            self.length = 1
            self.initialized = True

        else:
            self.winner = parent.winner
            self.player = P2 if parent.player == P1 else P1
            self.length = parent.length+1

            if move is not None and not self.capturedQuadrantEquals(move[1], True):
                nextQuadrant = move[1]

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

        if self.move is not None and not self.moveSet:
            currentQuadrant = np.zeros(9, dtype=int)
            self.buildQuadrant(currentQuadrant, self.move[0])
            self.capturedQuadrant = check3InRow(currentQuadrant)

            if self.capturedQuadrant != N:
                allQuadrants = np.zeros(9, dtype=int)
                self.buildQuadrant(allQuadrants)
                self.winner = check3InRow(allQuadrants)


    
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
        return self.move[0]

    
    def getLocal(self):
        return self.move[1]

    
    def getWinner(self):
        return self.winner

    
    def getNextQuadrant(self):
        return self.nextQuadrant


    def __len__(self):
        return self.length

    def getPlayer(self):
        return self.player

    def getParent(self):
        return self.parent

    def hasChildren(self):
        return self.children is not None

    def getChildren(self):
        return self.children

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


    
    def buildQuadrant(self, array, quadrant = None):
        current = self
        if quadrant is None:
            while True:
                if current.capturedQuadrant != N:
                    array[current.move[0]] = current.capturedQuadrant

                current = current.parent

                if current is None:
                    break

        else:
            while True:
                if current.move is not None and current.move[0] == quadrant:
                    array[current.move[1]] = current.player

                current = current.parent

                if current is None:
                    break


    
    def buildBoard2D(self, array):
        current = self
        while True:
            if current.move is not None:
                array[current.move[0]][current.move[1]] = current.player

            current = current.parent

            if current is None:
                break



if __name__ == "__main__":
    node = UTTT_Node()
