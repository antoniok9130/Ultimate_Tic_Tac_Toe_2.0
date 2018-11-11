import time

import numpy as np
import torch

import sys
sys.path.append("..\\..\\")

from UTTT import *
from Policy_Model import *



class NN_MCTS:
    def __init__(self, model1=None, model2=None):
        self.model1 = model1
        self.model2 = model2

        if self.model1 is None:
            self.model1 = Policy_Model("./ModelInstances/policy1/policy1_model")

        if self.model2 is None:
            self.model2 = Policy_Model("./ModelInstances/policy2/policy2_model")

        self.player = None

        self.getChildHighestUCT = getChildHighestUCT
        self.getChildVisitedMost = getChildVisitedMost
        self.select = select
        self.expand = expand


    def getMove(self, node, iterations=3200):
        getMove(node, iterations=iterations, select=self.select, runSimulation=self.runSimulation)



    def runSimulation(self, node):
        node.init()
        board = node.buildBoard2D()
        quadrants = node.buildQuadrants()
        
        input_tensor = torch.from_numpy(extract_features(quadrants, board))

        if self.player == P1:
            return list(self.model1.predict(input_tensor))

        else:
            return list(self.model2.predict(input_tensor))

