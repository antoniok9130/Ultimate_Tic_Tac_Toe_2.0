# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from UTTT import UTTT

P1 = UTTT.P1
P2 = UTTT.P2


class MCTSPlayer:
    def __init__(self, game):
        self.game = game

    def start_turn(self):
        self.game.game.runIterations(2000000)
        self.game.game.make_move()
        self.game.next()
