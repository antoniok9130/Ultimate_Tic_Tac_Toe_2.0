
from .utils import *
from .Node import *
from .Logic import *

import numpy as np

class UTTT_Environment:

    def __init__(self):
        self.finished = False
        self.reset()

    def step(self, action):
        self.reward = 0
        self.done = False
        self.legal = action in self.legalMoves
        if self.legal:
            g = action[0]
            l = action[1]

            self.player = P2 if self.player == P1 else P1
            self.board[g][l] = self.player
            self.numBoardRemaining[g] -= 1
            if check3InRowAt(self.board[g], l):
                self.quadrants[g] = self.player
                self.numQuadrantsRemaining -= 1

                if check3InRowAt(self.quadrants, g):
                    self.reward += 1
                    self.done = True
                
                elif self.numQuadrantsRemaining < 1:
                    self.done = True

            elif self.numBoardRemaining[g] < 1:
                self.quadrants[g] = self.player
                self.numQuadrantsRemaining -= 1
                
                if self.numQuadrantsRemaining < 1:
                    self.done = True

            self.previousMove = action

        return self.return_observation()

    def return_observation(self):
        return self.board, self.reward, self.done, {"legal": self.legal, "player": self.player}

    def random_action(self):
        return self.legalMoves[np.random.randint(len(self.legalMoves))]

    
    def additional_reset(self):
        pass
                    
            
    def reset(self):
        self.board = np.zeros((9, 9))
        self.quadrants = np.zeros(9)
        self.previousMove = None
        self.numQuadrantsRemaining = 9
        self.numBoardRemaining = [9 for _ in range(9)]
        self.player = N
        self.legalMoves = getLegalMoves2D(self.quadrants, self.board, self.previousMove)
        self.additional_reset()
        return self.board

def flatten_move(move):
    return 9*move[0]+move[1]

def unflatten_move(move):
    return [int(move//9), int(move%9)]
