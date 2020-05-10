# -*- coding: utf-8 -*-
import sys

sys.path.append("../../UTTT/Python")

from MCTS import MCTS


if __name__ == "__main__":
    m = MCTS()
    s = m.select()
    e = s.expand()
    w = e.simulate()
    e.backprop(w)
