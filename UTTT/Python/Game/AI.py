# -*- coding: utf-8 -*-
from time import time

from ..MCTS import getHardcodedSecondMove
from .Player import Player
from .UI import sleep


class MCTSPlayer(Player):
    def __init__(self, game, ui=False):
        super().__init__(game, ui)
        self.first_turn = True

    def start_turn(self):
        self.update()
        sleep(0.1)

        if self.first_turn:
            self.first_turn = False
            if self.game.game.empty:
                self.game.game.choose_move(4, 4)
            else:
                ij = getHardcodedSecondMove(*self.game.game.move)
                i = ij // 9
                j = ij % 9
                self.game.game.choose_move(i, j)

            sleep(1)
        else:
            start = time()

            # self.game.game.runParallelIterations(2500000)
            self.game.game.runIterations(2500000)

            end = time()

            self.game.game.make_move()

            print("Thinking Time: ", (end - start), "seconds")
            print(
                f"Confidence:  {self.game.game.num_wins / self.game.game.num_visits:2%}"
            )

        self.update()
        sleep(0.1)
        self.game.next()
