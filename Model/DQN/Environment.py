import sys
sys.path.append("../../")

from UTTT.utils import *
from APVMCTS import *
from UTTT.Logic import *
from UTTT.second_move import * 

import numpy as np

class UTTT_Environment:

    def __init__(self):
        self.finished = False
        self.reset()

    def step(self, action):
        self.reward = 0
        self.done = False
        self.legal = self.node.isLegal(action, raise_exception=True)
        if self.legal:
            g = action[0]
            l = action[1]

            self.node.setChild(action)
            self.node = self.node.getChild(0)
            self.board[int(3*(g//3)+l//3)][int(3*(g%3)+l%3)] = self.node.getPlayer()
            
            self.node.init()
            self.winner = self.node.winner
            if self.winner != N:
                self.done = True

            self.moves.append(action)

        return self.return_observation()

    def return_observation(self):
        return self.board, self.reward, self.done, {"legal": self.legal}

    
    def additional_reset(self):
        # action = unflatten_move(np.random.randint(81))
        # self.step(action)
        # action = get_second_move(*action)
        # self.step(action)
        pass
            
    def reset(self):
        self.board = np.zeros((9, 9))
        self.winner = 0
        self.moves = []
        self.node = APVMCTS_Node(0)
        self.additional_reset()
        return self.board

    def get_action(self, model, device, iterations=100):
        return getMove(self.node, model, device, iterations=iterations)


# if __name__ == "__main__":
#     board = np.zeros((9, 9))
#     for g in range(9):
#         for l in range(9):
#             # print(g, l, 3*(g//3)+l//3, 3*(g%3)+l%3)
#             # board[int(3*(g//3)+l//3)][int(3*(g%3)+l%3)] = 9*g+l
#             board[g][l] = 9*g+l

#     print(board)
#     board = np.array(unravel_board(board))

#     print(board)