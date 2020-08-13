# -*- coding: utf-8 -*-
from ..UTTT import UTTT
from .Player import Player


class HumanPlayer(Player):
    def __init__(self, game, ui=False):
        super().__init__(game, ui)
        self.move = []

    def start_turn(self):
        self.update()
        if self.game.get_winner() == UTTT.N:
            self.ui.unlock()
        else:
            self.ui.lock()

    def end_turn(self):
        self.game.make_move(*self.move)
        self.update()
        self.ui.lock()
        self.game.next()
