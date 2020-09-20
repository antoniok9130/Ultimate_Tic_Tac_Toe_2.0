# -*- coding: utf-8 -*-
import sys

sys.path.append("../../UTTT/Python")

from UTTT import UTTT


if __name__ == "__main__":
    uttt = UTTT()
    uttt.move = (0, 1)
    uttt.move = (1, 2)
    uttt.move = (2, 3)
    uttt.move = (3, 4)
    uttt.move = (4, 5)
    uttt.move = (5, 6)
    uttt.move = (6, 7)
    uttt.move = (7, 8)
    uttt.move = (8, 0)
    print(uttt)

    uttt.rotate(k=1)
    print(uttt)
