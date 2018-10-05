from math import sqrt, log

from UTTT_Node import *


class MCTS_Node(UTTT_Node):

    def __init__(self, move = None, parent = None, initialize = False):
        super().__init__(move, parent, initialize)

        self.numWins = 0
        self.numVisits = 0
        self.UCT = 100


    def updateUCT(self):
        if self.parent is not None and self.numVisits != 0:
            self.UCT = self.numWins/self.numVisits + sqrt(2*log(self.parent.getNumVisits())/self.numVisits)


    def getUCT(self):
        return self.UCT

    def getNumWins(self):
        return self.numWins

    def getNumVisits(self):
        return self.numVisits

    def incrementWins(self, num = 1):
        self.numWins += num

    def incrementVisits(self, num = 1):
        self.numVisits += num


    def getConfidence(self):
        return self.numWins/self.numVisits