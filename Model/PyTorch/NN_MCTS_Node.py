from math import sqrt, log

import sys
sys.path.append("..\..\Game\Python")

from UTTT_Node import *


class NN_MCTS_Node(UTTT_Node):

    def __init__(self, move = None, parent = None, initialize = False):
        super().__init__(move, parent, initialize)

        # self.winProb = 0
        # self.loseProb = 0
        self.numWins = 0
        self.numVisits = 0
        self.UCT = 100


    def updateUCT(self, probabilities):
        winProb = probabilities[0 if self.player == P1 else 1]
        loseProb = probabilities[1 if self.player == P1 else 0]
        # self.winProb += winProb
        # self.loseProb += loseProb
        if winProb > loseProb:
            self.numWins += 1
        self.numVisits += 1

        if self.parent is not None:
            # (self.winProb - self.loseProb) + 
            self.UCT = self.numWins/self.numVisits + sqrt(2*log(self.parent.getNumVisits())/self.numVisits)


    def getUCT(self):
        return self.UCT

    # def getWinProb(self):
    #     return self.winProb

    # def getLoseProb(self):
    #     return self.loseProb

    def getNumWins(self):
        return self.numWins

    def getNumVisits(self):
        return self.numVisits


    def getConfidence(self):
        return self.numWins/self.numVisits