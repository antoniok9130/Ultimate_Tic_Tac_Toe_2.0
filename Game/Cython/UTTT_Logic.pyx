#cython: language_level=3, boundscheck=False

import numpy as np

P1 = 1
P2 = 2
N = 0
T = -1
B = 3 # Note that (P1 | P2) == B

cdef tuple triple0 = ((1, 2), (3, 6))
cdef tuple triple4 = ((3, 5), (1, 7), (0, 8), (2, 6))
cdef tuple triple8 = ((6, 7), (2, 5))

pairs = (((1, 2), (3, 6), (4, 8)),
        ((0, 2), (4, 7)),
        ((0, 1), (5, 8), (4, 6)),
        ((0, 6), (4, 5)),
        ((0, 8), (1, 7), (2, 6), (3, 5)),
        ((2, 8), (3, 4)),
        ((0, 3), (2, 4), (7, 8)),
        ((1, 4), (6, 8)),
        ((6, 7), (2, 5), (0, 4)))

def check3InRow(array, position = None):
    if (position != None):
        for p0, p1 in pairs[position]:
            if (array[position] == array[p0] and array[p0] == array[p1]):
                return True

        return False

    cdef int checkTie = 1
    if (array[0] != N):
        for t1, t2 in triple0:
            if (array[0] == array[t1] and array[t1] == array[t2]):
                return array[0]
    else:
        checkTie = 0

    if (array[4] != N):
        for t1, t2 in triple4:
            if (array[4] == array[t1] and array[t1] == array[t2]):
                return array[4]
    else:
        checkTie = 0

    if (array[8] != N):
        for t1, t2 in triple8:
            if (array[8] == array[t1] and array[t1] == array[t2]):
                return array[8]
    else:
        checkTie = 0

    return T if (checkTie == 1 and array[1] != N and array[2] != N and array[3] != N and
                                   array[5] != N and array[6] != N and array[7] != N) \
             else N


def checkTie(array):
    for i in array:
        if (i == N):
            return False

    return True


symbols = {P1:"X", P2:"O", T:"T"}

def getBoardSymbol(int value, simple = True):
    if (value in symbols):
        return symbols[value]

    return "_" if simple else " "


def getRandomRemaining(quadrant):
    for r in np.random.randint(low=0, high=9, size=100):
        if (quadrant[r] == N):
            return r

    print("Could not find Random Remaining for:  {0}".format(quadrant))
    print(quadrant[0] == N)
    exit(1)



cdef str verticalSpace = "     │   │    ║    │   │    ║    │   │    "
cdef str verticalDivide = "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── "
cdef str bigVerticalDivide = " ═════════════╬═════════════╬═════════════"

def printBoard(board, quadrant, simple = False):
    if simple:
        for a in range(3) :
            for b in range(3) :
                for c in range(3) :
                    for d in range(3):
                        print(getBoardSymbol(board[3 * a + c][3 * b + d], simple), end="")

                    print("  ", end="")

                if (a == 0) :
                    print("   ", end="")
                    for d in range(3):
                        print(getBoardSymbol(quadrant[3 * b + d], simple))

                print()

            print()

    else :
        print()
        for a in range(3):
            if (a != 0):
                print(bigVerticalDivide)

            print(verticalSpace)
            for b in range(3):
                if (b != 0):
                    print(verticalDivide)

                print("  ", end="")
                for c in range(3):
                    if (c != 0):
                        print(" ║ ", end="")

                    for d in range(3):
                        if (d != 0):
                            print("│", end="")

                        print(" "+getBoardSymbol(board[3 * a + c][3 * b + d], simple)+" ", end="")


                print(" ")

            print(verticalSpace)

        print()






