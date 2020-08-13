# -*- coding: utf-8 -*-
from ..UTTT import UTTT
from .UI import UTTT_Widget

P1 = UTTT.P1
P2 = UTTT.P2
N = UTTT.N
T = UTTT.T


class Player:
    def __init__(self, game, ui=False):
        self.game = game

        if ui:
            self.ui = UTTT_Widget(self)
            self.ui.show()
        else:
            self.ui = None

    def update(self):
        if self.ui:
            if self.game.get_winner() != N:
                if self.game.get_winner() == T:
                    self.ui.current_player = None
                else:
                    self.ui.current_player = self.game.get_winner()

                self.ui.legal_moves = {(i, j) for i in range(9) for j in range(9)}
            else:
                self.ui.current_player = self.game.get_current_player()
                self.ui.legal_moves = self.game.get_legal_moves()

            self.ui.filled = self.game.get_filled()
            self.ui.quadrant_filled = self.game.get_quadrant_filled()

            self.ui.update()
            self.ui.repaint()
