# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

from .Human import HumanPlayer
from .AI import MCTSPlayer

from ..MCTS import MCTS
from ..UTTT import UTTT


class Game:
    def __init__(self, Player1, Player2):
        self.game = MCTS()
        self.player1 = Player1(self, ui=True)
        self.player2 = Player2(self, ui=False)

    def start(self):
        self.next()

    def make_move(self, g, l):
        self.game.choose_move(g, l)

    def next(self):
        if self.get_current_player() == UTTT.P2:
            self.player2.start_turn()
        else:
            self.player1.start_turn()

    def get_current_player(self):
        if self.game.player == UTTT.P2:
            return UTTT.P1
        else:
            return UTTT.P2

    def get_legal_moves(self):
        return {(i, j) for i in range(9) for j in range(9) if self.game.is_legal(i, j)}

    def get_filled(self):
        return self.game.get_filled()

    def get_quadrant_filled(self):
        return {(i, self.game[i]) for i in range(9) if self.game[i] != UTTT.N}

    def get_winner(self):
        return self.game.winner


def play():
    app = QApplication(sys.argv)
    game = Game(HumanPlayer, MCTSPlayer)
    game.start()
    sys.exit(app.exec_())
