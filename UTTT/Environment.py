
from .utils import *
from .Node import *
from .Logic import *

import numpy as np

class UTTT_Environment:

    def __init__(self):
        self.reset()

    def step(self, action):
        reward = 0
        done = False
        legal = tuple(action) in self.legalMoves
        if legal:
            g = action[0]
            l = action[1]

            self.player = P1 if self.player == P2 else P2
            self.board[g][l] = self.player
            self.numBoardRemaining[g] -= 1
            if check3InRowAt(self.board[g], l):
                self.quadrants[g] = self.player
                reward += 10

                self.numQuadrantsRemaining -= 1

                if check3InRowAt(self.quadrants, g):
                    reward += 90
                    done = True
                
                elif self.numQuadrantsRemaining < 1:
                    done = True
                    reward += 15

            elif self.numBoardRemaining[g] < 1:
                self.quadrants[g] = T
                self.numQuadrantsRemaining -= 1
                
                if self.numQuadrantsRemaining < 1:
                    done = True
                    reward += 15


            if not done and self.quadrants[l] != N:
                reward -= 1

            self.previousMove = action

        return self.board, reward, done, {"legal": legal}


    def random_action(self):
        return self.legalMoves[np.random.randint(len(self.legalMoves))]
                    
            
    def reset(self):
        self.board = np.zeros((9, 9))
        self.quadrants = np.zeros(9)
        self.previousMove = None
        self.numQuadrantsRemaining = 9
        self.numBoardRemaining = [9 for _ in range(9)]
        self.player = N
        self.legalMoves = getLegalMoves2D(self.quadrants, self.board, self.previousMove)
        return self.board

def flatten_move(move):
    return 9*move[0]+move[1]

def unflatten_move(move):
    return [int(move//9), int(move%9)]
