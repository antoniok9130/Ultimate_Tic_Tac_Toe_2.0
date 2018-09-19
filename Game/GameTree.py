from numpy import array as np_array

import Model.TensorFlow.ZeroNetwork as zn
from Game.UTTT import UTTT


class GameNode:
    def __init__(self, global_move=None, local_move=None, parent=None):
        self.parent = parent

        # self.prior_probability = None
        self.score = None
        self.action_value_Q = 0
        self.visit_count_N = 0

        self.game = UTTT() if (parent is None) else UTTT(parent.game)
        if global_move is not None and local_move is not None:
            self.game.add_move(global_move, local_move)
            self.action_value_Q = zn.valuate(zn.model.eval(
                feed_dict={zn.input:np_array([self.game.board.board]), zn.keep_prob:1}))
            self.increment_visit_count()
        self.children = None

    def increment_visit_count(self):
        self.visit_count_N += 1
        self.update_score()

    def update_score(self):
        self.score = self.action_value_Q + 1/(1+self.visit_count_N)

    def update_Q(self, V):
        self.action_value_Q = (self.action_value_Q*(self.visit_count_N-1)+V)/self.visit_count_N
        if self.parent is not None:
            self.parent.update_Q(V)

    def is_leaf(self):
        return self.children is None
    def expand_leaf(self):
        if self.is_leaf() and self.game.winner == 0:
            moves = []
            if self.game.gameLength == 0:
                moves = [[i, j] for i in range(9) for j in range(9)]
            elif self.game.grid3by3[self.game.moves[-1][1]] == 0:
                i = self.game.moves[-1][1]
                moves = [[i, j] for j in self.game.board2dLeft[i]]
            else:
                moves = [[i, j] for i in self.game.grid3by3Left
                         for j in self.game.board2dLeft[i]]

            self.children = [GameNode(move[0], move[1], self) for move in moves]
