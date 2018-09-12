#cython: language_level=3, boundscheck=False
from UTTT_Logic import *

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

def updatePotential3inRow(potential, array, position):
    cdef int player = array[position]
    if player != N:
        for p0, p1 in pairs[position]:
            if player == array[p0]:
                potential[p1] |= player
            elif player == array[p1]:
                potential[p0] |= player


