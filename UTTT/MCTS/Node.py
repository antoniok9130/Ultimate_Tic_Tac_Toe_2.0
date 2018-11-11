from numpy import sqrt, log

from ..Node import *


class MCTS_Node(UTTT_Node):

    def __init__(self, move = None, parent = None, initialize = False):
        super().__init__(move, parent, initialize)

        self.numWins = 0
        self.numVisits = 0
        self.UCT = 100
        self.oldUCT = True


    # def updateUCT(self):
    #     if self.parent is not None and self.numVisits != 0:
    #         self.UCT = self.numWins/self.numVisits + sqrt(2*log(self.parent.getNumVisits())/self.numVisits)


    def getUCT(self):
        if self.oldUCT:
            if self.parent is not None and self.numVisits != 0:
                self.UCT = calculateUCT(self.numWins, self.numVisits, self.parent.getNumVisits())
            else:
                self.UCT = 100
            self.oldUCT = False

        return self.UCT

    def getNumWins(self):
        return self.numWins

    def getNumVisits(self):
        return self.numVisits

    def incrementWins(self, num = 1):
        self.numWins += num
        self.oldUCT = True

    def incrementVisits(self, num = 1):
        self.numVisits += num
        self.oldUCT = True


    def getConfidence(self):
        return self.numWins/self.numVisits


@jit(cache=True, nopython=True)
def calculateUCT(numWins, numVisits, parent_numVisits):
    return numWins/numVisits + sqrt(2*log(parent_numVisits)/numVisits)