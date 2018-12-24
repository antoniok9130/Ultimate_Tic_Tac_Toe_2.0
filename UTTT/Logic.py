# import sys

from numba import jit
from numpy import array as np_array, zeros as np_zeros, intc, flatnonzero
from numpy.random import seed as np_seed, choice as np_choice, randint as randint
import numpy as np

from .utils import *


P1 = 1
P2 = 2
N = 0
T = -1
B = (P1 | P2) # Note that (P1 | P2) == B

if B == P1 or B == P2 or B == N or B == T:
    raise Exception("B == P1 or B == P2 or B == N or B == T")

triple0 = np_array([[1, 2], [3, 6]])
triple4 = np_array([[3, 5], [1, 7], [0, 8], [2, 6]])
triple8 = np_array([[6, 7], [2, 5]])

pairs = np_array([[[1, 2], [3, 6], [4, 8]],
                  [[0, 2], [4, 7]],
                  [[0, 1], [5, 8], [4, 6]],
                  [[0, 6], [4, 5]],
                  [[0, 8], [1, 7], [2, 6], [3, 5]],
                  [[2, 8], [3, 4]],
                  [[0, 3], [2, 4], [7, 8]],
                  [[1, 4], [6, 8]],
                  [[6, 7], [2, 5], [0, 4]]])

def check3InRow(array):

    checkTie = True
    if (array[0] != N):
        for triple in triple0:
            if (array[0] == array[triple[0]] and array[triple[0]] == array[triple[1]]):
                return array[0]

    else:
        checkTie = False

    if (array[4] != N):
        for triple in triple4:
            if (array[4] == array[triple[0]] and array[triple[0]] == array[triple[1]]):
                return array[4]

    else:
        checkTie = False

    if (array[8] != N):
        for triple in triple8:
            if (array[8] == array[triple[0]] and array[triple[0]] == array[triple[1]]):
                return array[8]

    else:
        checkTie = False

    return T if (checkTie and array[1] != N and array[2] != N and array[3] != N and
                              array[5] != N and array[6] != N and array[7] != N) \
             else N


@jit(cache=True, nopython=True)
def check3InRowAt(array, position):
    # for i, pair in enumerate(pairs):
    #     print(f"if position == {i}:")
    #     print(f"    return {' or '.join(f'array[{i}] == array[{p0}] == array[{p1}]' for p0, p1 in pair)}\n")

    if position == 0:
        return array[0] == array[1] == array[2] or array[0] == array[3] == array[6] or array[0] == array[4] == array[8]

    if position == 1:
        return array[1] == array[0] == array[2] or array[1] == array[4] == array[7]

    if position == 2:
        return array[2] == array[0] == array[1] or array[2] == array[5] == array[8] or array[2] == array[4] == array[6]

    if position == 3:
        return array[3] == array[0] == array[6] or array[3] == array[4] == array[5]

    if position == 4:
        return array[4] == array[0] == array[8] or array[4] == array[1] == array[7] or array[4] == array[2] == array[6] or array[4] == array[3] == array[5]

    if position == 5:
        return array[5] == array[2] == array[8] or array[5] == array[3] == array[4]

    if position == 6:
        return array[6] == array[0] == array[3] or array[6] == array[2] == array[4] or array[6] == array[7] == array[8]

    if position == 7:
        return array[7] == array[1] == array[4] or array[7] == array[6] == array[8]

    if position == 8:
        return array[8] == array[6] == array[7] or array[8] == array[2] == array[5] or array[8] == array[0] == array[4]

    # for p0, p1 in pairs[position]:
    #     if (array[position] == array[p0] and array[p0] == array[p1]):
    #         return True

    # return False



def getLegalMoves2D(quadrants, board, previousMove):
    return [[int(m//9), int(m%9)] for m in getLegalMoves1D(quadrants, board, previousMove)]


def getLegalMoves1D(quadrants, board, previousMove):
    return np.nonzero(getLegalMovesField(quadrants, board, previousMove))[0].tolist()


@jit(cache=True)
def getLegalMovesField(quadrants, board, previousMove):
    legalMoves = np.zeros(81)
    getLegalMovesField_numba(legalMoves, quadrants, board, [-1, -1] if previousMove is None else previousMove)
    return legalMoves

@jit(cache=True, nopython=True)
def getLegalMovesField_numba(legalMoves, quadrants, board, previousMove):
    if previousMove[1] != -1 and quadrants[previousMove[1]] == N:
        g = 9*previousMove[1]
        for l, q in enumerate(board[previousMove[1]]):
            if q == N:
                legalMoves[g+l] = 1.0
    else:
        for g, aQ in enumerate(quadrants):
            if aQ == N:
                for l, b_gl in enumerate(board[g]):
                    if b_gl == N:
                        legalMoves[9*g+l] = 1.0


@jit(cache=True, nopython=True)
def potential3inRow(array, position):
    
    # for i, pair in enumerate(pairs):
    #     print(f"if position == {i}:")
    #     for p0, p1 in pair:
    #         print(f"    if array[{p0}] != N and array[{p0}] == array[{p1}]:")
    #         print(f"        if potential != N and potential != array[{p0}]:")
    #         print(f"            return B")
    #         print(f"        potential = array[{p0}]")
    #     print("    return potential\n")

    potential = N

    if position == 0:
        if array[1] != N and array[1] == array[2]:
            if potential != N and potential != array[1]:
                return B
            potential = array[1]
        if array[3] != N and array[3] == array[6]:
            if potential != N and potential != array[3]:
                return B
            potential = array[3]
        if array[4] != N and array[4] == array[8]:
            if potential != N and potential != array[4]:
                return B
            potential = array[4]
        return potential

    if position == 1:
        if array[0] != N and array[0] == array[2]:
            if potential != N and potential != array[0]:
                return B
            potential = array[0]
        if array[4] != N and array[4] == array[7]:
            if potential != N and potential != array[4]:
                return B
            potential = array[4]
        return potential

    if position == 2:
        if array[0] != N and array[0] == array[1]:
            if potential != N and potential != array[0]:
                return B
            potential = array[0]
        if array[5] != N and array[5] == array[8]:
            if potential != N and potential != array[5]:
                return B
            potential = array[5]
        if array[4] != N and array[4] == array[6]:
            if potential != N and potential != array[4]:
                return B
            potential = array[4]
        return potential

    if position == 3:
        if array[0] != N and array[0] == array[6]:
            if potential != N and potential != array[0]:
                return B
            potential = array[0]
        if array[4] != N and array[4] == array[5]:
            if potential != N and potential != array[4]:
                return B
            potential = array[4]
        return potential

    if position == 4:
        if array[0] != N and array[0] == array[8]:
            if potential != N and potential != array[0]:
                return B
            potential = array[0]
        if array[1] != N and array[1] == array[7]:
            if potential != N and potential != array[1]:
                return B
            potential = array[1]
        if array[2] != N and array[2] == array[6]:
            if potential != N and potential != array[2]:
                return B
            potential = array[2]
        if array[3] != N and array[3] == array[5]:
            if potential != N and potential != array[3]:
                return B
            potential = array[3]
        return potential

    if position == 5:
        if array[2] != N and array[2] == array[8]:
            if potential != N and potential != array[2]:
                return B
            potential = array[2]
        if array[3] != N and array[3] == array[4]:
            if potential != N and potential != array[3]:
                return B
            potential = array[3]
        return potential

    if position == 6:
        if array[0] != N and array[0] == array[3]:
            if potential != N and potential != array[0]:
                return B
            potential = array[0]
        if array[2] != N and array[2] == array[4]:
            if potential != N and potential != array[2]:
                return B
            potential = array[2]
        if array[7] != N and array[7] == array[8]:
            if potential != N and potential != array[7]:
                return B
            potential = array[7]
        return potential

    if position == 7:
        if array[1] != N and array[1] == array[4]:
            if potential != N and potential != array[1]:
                return B
            potential = array[1]
        if array[6] != N and array[6] == array[8]:
            if potential != N and potential != array[6]:
                return B
            potential = array[6]
        return potential

    if position == 8:
        if array[6] != N and array[6] == array[7]:
            if potential != N and potential != array[6]:
                return B
            potential = array[6]
        if array[2] != N and array[2] == array[5]:
            if potential != N and potential != array[2]:
                return B
            potential = array[2]
        if array[0] != N and array[0] == array[4]:
            if potential != N and potential != array[0]:
                return B
            potential = array[0]
        return potential

    # for p0, p1 in pairs[position]:
    #     if array[p0] != N and array[p0] == array[p1]:
    #         if potential != N and potential != array[p0]:
    #             potential = B
    #             break

    #         potential = array[p0]

    return potential


@jit(cache=True, nopython=True)
def potential3inRow_wp(array, position, player):
    # for i, pair in enumerate(pairs):
    #     print(f"if position == {i}:")
    #     print(f"    return {' or '.join(f'player == array[{p0}] == array[{p1}]' for p0, p1 in pair)}\n")

    if position == 0:
        return player == array[1] == array[2] or player == array[3] == array[6] or player == array[4] == array[8]

    if position == 1:
        return player == array[0] == array[2] or player == array[4] == array[7]

    if position == 2:
        return player == array[0] == array[1] or player == array[5] == array[8] or player == array[4] == array[6]

    if position == 3:
        return player == array[0] == array[6] or player == array[4] == array[5]

    if position == 4:
        return player == array[0] == array[8] or player == array[1] == array[7] or player == array[2] == array[6] or player == array[3] == array[5]

    if position == 5:
        return player == array[2] == array[8] or player == array[3] == array[4]

    if position == 6:
        return player == array[0] == array[3] or player == array[2] == array[4] or player == array[7] == array[8]

    if position == 7:
        return player == array[1] == array[4] or player == array[6] == array[8]

    if position == 8:
        return player == array[6] == array[7] or player == array[2] == array[5] or player == array[0] == array[4]

    # for p0, p1 in pairs[position]:
    #     if array[p0] == player and array[p0] == array[p1]:
    #         return True

    # return False


@jit(cache=True, nopython=True)
def updatePotential3inRow(potential, array, position):
    player = array[position]
    if player != N:

        # for i, pair in enumerate(pairs):
        #     print(f"if position == {i}:")
        #     for p0, p1 in pair:
        #         print(f"    if player == array[{p0}]:")
        #         print(f"        potential[{p1}] |= player")
        #         print(f"    if player == array[{p1}]:")
        #         print(f"        potential[{p0}] |= player")
        #     print()

        if position == 0:
            if player == array[1]:
                potential[2] |= player
            if player == array[2]:
                potential[1] |= player
            if player == array[3]:
                potential[6] |= player
            if player == array[6]:
                potential[3] |= player
            if player == array[4]:
                potential[8] |= player
            if player == array[8]:
                potential[4] |= player

        if position == 1:
            if player == array[0]:
                potential[2] |= player
            if player == array[2]:
                potential[0] |= player
            if player == array[4]:
                potential[7] |= player
            if player == array[7]:
                potential[4] |= player

        if position == 2:
            if player == array[0]:
                potential[1] |= player
            if player == array[1]:
                potential[0] |= player
            if player == array[5]:
                potential[8] |= player
            if player == array[8]:
                potential[5] |= player
            if player == array[4]:
                potential[6] |= player
            if player == array[6]:
                potential[4] |= player

        if position == 3:
            if player == array[0]:
                potential[6] |= player
            if player == array[6]:
                potential[0] |= player
            if player == array[4]:
                potential[5] |= player
            if player == array[5]:
                potential[4] |= player

        if position == 4:
            if player == array[0]:
                potential[8] |= player
            if player == array[8]:
                potential[0] |= player
            if player == array[1]:
                potential[7] |= player
            if player == array[7]:
                potential[1] |= player
            if player == array[2]:
                potential[6] |= player
            if player == array[6]:
                potential[2] |= player
            if player == array[3]:
                potential[5] |= player
            if player == array[5]:
                potential[3] |= player

        if position == 5:
            if player == array[2]:
                potential[8] |= player
            if player == array[8]:
                potential[2] |= player
            if player == array[3]:
                potential[4] |= player
            if player == array[4]:
                potential[3] |= player

        if position == 6:
            if player == array[0]:
                potential[3] |= player
            if player == array[3]:
                potential[0] |= player
            if player == array[2]:
                potential[4] |= player
            if player == array[4]:
                potential[2] |= player
            if player == array[7]:
                potential[8] |= player
            if player == array[8]:
                potential[7] |= player

        if position == 7:
            if player == array[1]:
                potential[4] |= player
            if player == array[4]:
                potential[1] |= player
            if player == array[6]:
                potential[8] |= player
            if player == array[8]:
                potential[6] |= player

        if position == 8:
            if player == array[6]:
                potential[7] |= player
            if player == array[7]:
                potential[6] |= player
            if player == array[2]:
                potential[5] |= player
            if player == array[5]:
                potential[2] |= player
            if player == array[0]:
                potential[4] |= player
            if player == array[4]:
                potential[0] |= player

        # for pair in pairs[position]:
        #     if player == array[pair[0]]:
        #         potential[pair[1]] |= player
        #     elif player == array[pair[1]]:
        #         potential[pair[0]] |= player


def isNextWin(node):
    AIPlayer = P2 if node.getPlayer() == P1 else P1
    quadrants = node.buildQuadrant()
    if node.nextQuadrant != -1:
        if potential3inRow_wp(quadrants, node.nextQuadrant, AIPlayer):
            quadrant = node.buildQuadrant(quadrant=node.nextQuadrant)
            for i, q in enumerate(quadrant):
                if q == N and potential3inRow_wp(quadrant, i, AIPlayer):
                    return [node.nextQuadrant, i]

    else:
        for i, q in enumerate(quadrants):
            if q == N and potential3inRow_wp(quadrants, i, AIPlayer):
                quadrant = node.buildQuadrant(quadrant=i)
                for j, q1 in enumerate(quadrant):
                    if q1 == N and potential3inRow_wp(quadrant, j, AIPlayer):
                        return [i, j]

    return None


def getBoardSymbol(value, simple = True):
    if (value == P1):
        return "X"
    if (value == P2):
        return "O"
    if (value == T):
        return "T"

    return "_" if simple else " "


np_seed(current_time_milli()%(2**32-1))

@jit(cache=True, nopython=True)
def getRandomRemaining(quadrant):
    choices = randint(9)
    i = 0
    while i < 900:
        r = randint(9)
        if (quadrant[r] == N):
            return r
        i += 1

    raise Exception("Could not find Random Remaining")

    # return np_choice(flatnonzero(quadrant == N))
    
    # choices = randint(9, size=36)
    # for r in choices:
    #     if (quadrant[r] == N):
    #         return r

    # return np_choice(flatnonzero(quadrant == N))


@jit(cache=True, nopython=True)
def checkInstantWin(potentialQuadrants, quadrants, board, g, player):
    if quadrants[g] == N and potentialQuadrants[g] == player or potentialQuadrants[g] == B:
        
        # for l in range(9):
        #     print(f"if board[g][{l}] == N and check3InRowAt(board[g], {l}):")
        #     print(f"    return True")

        if board[g][0] == N and check3InRowAt(board[g], 0):
            return True
        if board[g][1] == N and check3InRowAt(board[g], 1):
            return True
        if board[g][2] == N and check3InRowAt(board[g], 2):
            return True
        if board[g][3] == N and check3InRowAt(board[g], 3):
            return True
        if board[g][4] == N and check3InRowAt(board[g], 4):
            return True
        if board[g][5] == N and check3InRowAt(board[g], 5):
            return True
        if board[g][6] == N and check3InRowAt(board[g], 6):
            return True
        if board[g][7] == N and check3InRowAt(board[g], 7):
            return True
        if board[g][8] == N and check3InRowAt(board[g], 8):
            return True

        # for l in range(9):
        #     if board[g][l] == N and check3InRowAt(board[g], l):
        #         return True

    return False


# @jit(cache=True)
# def simulation(state, policy):

#     quadrants = state.buildQuadrant()
#     board     = state.buildBoard2D()

#     return jit_simulation(quadrants, board, state.winner, state.move, state.getPlayer(), policy)


@jit(cache=True) # , nopython=True
def simulation(quadrants, board, winner, move, player, length, policy):
    """
    Parameters
    ----------
    state : UTTT_Node
        The game state
    policy
    """

    numRemainingQuadrants = 0
    numRemainingBoard = np_zeros(9, dtype=intc)
    potentialQuadrants = np_zeros(9, dtype=intc)

    for i, quadrant in enumerate(quadrants):
        if quadrant == N:
            numRemainingQuadrants += 1
            potentialQuadrants[i] = potential3inRow(quadrants, i)
            for j in board[i]:
                if j == N:
                    numRemainingBoard[i] += 1

    length = -1

    while winner == N:
        length += 1

        if move is not None and quadrants[move[1]] == N:
            if checkInstantWin(potentialQuadrants, quadrants, board, move[1], player):
                winner = player
                break
        
        else:
            for g in range(9):
                if checkInstantWin(potentialQuadrants, quadrants, board, g, player):
                    winner = player
                    break

            if winner != N:
                break

        # try:
        policy(move, quadrants, board, length)
        g = move[0]
        l = move[1]
        # except:
        #     print(move)
        #     print(quadrants)
        #     print(numRemainingBoard)
        #     printBoard(board, quadrants)
        #     raise Exception("Exception was thrown")

        board[g][l] = player
        numRemainingBoard[g] -= 1

        if check3InRowAt(board[g], l):
            quadrants[g] = player
            numRemainingQuadrants -= 1
            numRemainingBoard[g] = 0

            updatePotential3inRow(potentialQuadrants, quadrants, g)

            if check3InRowAt(quadrants, g):
                winner = player
                break

            elif numRemainingQuadrants == 0:
                winner = T
                break

        elif numRemainingBoard[g] <= 0:
            quadrants[g] = T
            numRemainingQuadrants -= 1
            numRemainingBoard[g] = 0

            if numRemainingQuadrants == 0:
                winner = T
                break


        player = P2 if player == P1 else P1

    return winner, length


# verticalSpace = "     │   │    ║    │   │    ║    │   │    "
# verticalDivide = "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── "
# bigVerticalDivide = " ═════════════╬═════════════╬═════════════"

def printBoard(board, quadrant, simple = False):
    if simple:
        print('''
          {b00}{b01}{b02}  {b10}{b11}{b12}  {b20}{b21}{b22}   
          {b03}{b04}{b05}  {b13}{b14}{b15}  {b23}{b24}{b25}             
          {b06}{b07}{b08}  {b16}{b17}{b18}  {b26}{b27}{b28}         {q0}{q1}{q2}
                                                                    {q3}{q4}{q5}
          {b30}{b31}{b32}  {b40}{b41}{b42}  {b50}{b51}{b52}         {q6}{q7}{q8}     
          {b33}{b34}{b35}  {b43}{b44}{b45}  {b53}{b54}{b55}
          {b36}{b37}{b38}  {b46}{b47}{b48}  {b56}{b57}{b58}

          {b60}{b61}{b62}  {b70}{b71}{b72}  {b80}{b81}{b82}
          {b63}{b64}{b65}  {b73}{b74}{b75}  {b83}{b84}{b85}
          {b66}{b67}{b68}  {b76}{b77}{b78}  {b86}{b87}{b88}
        '''.format(
            **{
                f"b{i}{j}": getBoardSymbol(board[i][j], simple) for i in range(9) for j in range(9)
            },
            **{
                f"q{i}": getBoardSymbol(quadrant[i], simple) for i in range(9)
            }
        ))

    else :
        print('''
            │   │    ║    │   │    ║    │   │    
          {b00} │ {b01} │ {b02}  ║  {b10} │ {b11} │ {b12}  ║  {b20} │ {b21} │ {b22}   
         ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼───
          {b03} │ {b04} │ {b05}  ║  {b13} │ {b14} │ {b15}  ║  {b23} │ {b24} │ {b25}                ║   ║  
         ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼───             {q0} ║ {q1} ║ {q2}
          {b06} │ {b07} │ {b08}  ║  {b16} │ {b17} │ {b18}  ║  {b26} │ {b27} │ {b28}            ════╬═══╬════
            │   │    ║    │   │    ║    │   │                {q3} ║ {q4} ║ {q5}
        ═════════════╬═════════════╬═════════════          ════╬═══╬════
            │   │    ║    │   │    ║    │   │                {q6} ║ {q7} ║ {q8}
          {b30} │ {b31} │ {b32}  ║  {b40} │ {b41} │ {b42}  ║  {b50} │ {b51} │ {b52}                ║   ║  
         ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── 
          {b33} │ {b34} │ {b35}  ║  {b43} │ {b44} │ {b45}  ║  {b53} │ {b54} │ {b55}
         ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼───
          {b36} │ {b37} │ {b38}  ║  {b46} │ {b47} │ {b48}  ║  {b56} │ {b57} │ {b58}
            │   │    ║    │   │    ║    │   │   
        ═════════════╬═════════════╬═════════════
            │   │    ║    │   │    ║    │   │   
          {b60} │ {b61} │ {b62}  ║  {b70} │ {b71} │ {b72}  ║  {b80} │ {b81} │ {b82}
         ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼───
          {b63} │ {b64} │ {b65}  ║  {b73} │ {b74} │ {b75}  ║  {b83} │ {b84} │ {b85}
         ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼───
          {b66} │ {b67} │ {b68}  ║  {b76} │ {b77} │ {b78}  ║  {b86} │ {b87} │ {b88}
            │   │    ║    │   │    ║    │   │   
        '''.format(
            **{
                f"b{i}{j}": getBoardSymbol(board[i][j], simple) for i in range(9) for j in range(9)
            },
            **{
                f"q{i}": getBoardSymbol(quadrant[i], simple) for i in range(9)
            }
        ))






