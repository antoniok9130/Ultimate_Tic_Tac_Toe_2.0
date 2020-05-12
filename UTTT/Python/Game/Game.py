# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from Human import HumanPlayer
from AI import MCTSPlayer

from MCTS import MCTS
from UTTT import UTTT


class Game:
    def __init__(self, Player1, Player2):
        self.player1 = Player1(self)
        self.player2 = Player2(self)
        self.game = MCTS()

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
        return {
            (i, j, self.game[i, j])
            for i in range(9)
            for j in range(9)
            if self.game[i, j] != UTTT.N
        }

    def get_quadrant_filled(self):
        return {(i, self.game[i]) for i in range(9) if self.game[i] != UTTT.N}

    def get_winner(self):
        return self.game.winner


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game(HumanPlayer, MCTSPlayer)
    game.start()
    sys.exit(app.exec_())
