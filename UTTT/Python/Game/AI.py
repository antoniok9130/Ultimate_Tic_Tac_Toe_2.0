# -*- coding: utf-8 -*-
from time import sleep

from ..UTTT import UTTT
from ..MCTS import getHardcodedMove

P1 = UTTT.P1
P2 = UTTT.P2


class MCTSPlayer:
    def __init__(self, game):
        self.game = game
        self.first_turn = True

    def start_turn(self):
        if self.first_turn:
            self.first_turn = False
            if self.game.game.empty:
                self.game.game.choose_move(4, 4)
            else:
                ij = getHardcodedMove(*self.game.game.move)
                i = ij // 9
                j = ij % 9
                self.game.game.choose_move(i, j)

            sleep(1)
        else:
            # self.game.game.runParallelIterations(2500000)
            self.game.game.runIterations(2000000)
            self.game.game.make_move()

        self.game.next()
