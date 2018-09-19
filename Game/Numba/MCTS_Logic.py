
from numba import jit, void, int32
from numba.types import Array

from Game.Numba.UTTT_Logic import *


@jit(nopython=True)
def potential3inRow(array, position, player = None):
    if player is None:
        potential = N
        for p0, p1 in pairs[position]:
            if array[p0] != N and \
                    array[p0] == array[p1]:
                if potential != N and potential != array[p0]:
                    return B

                potential = array[p0]

        return potential

    else:
        for p0, p1 in pairs[position]:
            if array[p0] == player and \
                    array[p0] == array[p1]:
                return True

        return False


@jit(void(Array(int32, 1, "A"), Array(int32, 1, "A"), int32))
def updatePotential3inRow(potential, array, position):
    player = array[position]
    if player != N:
        for pair in pairs[position]:
            if player == array[pair[0]]:
                potential[pair[1]] |= player
            elif player == array[pair[1]]:
                potential[pair[0]] |= player


