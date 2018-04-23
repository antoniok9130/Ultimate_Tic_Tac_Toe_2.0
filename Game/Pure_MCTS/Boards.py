from abc import ABC, abstractmethod
from copy import deepcopy

P1 = -1
P2 = 1
N = 0
T = 2


# doubles = [[0, 1],[1, 2],[0, 2],
#            [6, 7],[7, 8],[6, 8],
#            [0, 3],[3, 6],[0, 6],
#            [2, 5, 8],
#            [3, 4, 5],
#            [1, 4, 7],
#            [0, 4, 8],
#            [2, 4, 6]]


# def check_2_in_row(array):
#     for triple in triples:
#         if array[triple[0]] is not None and array[triple[0]] == array[triple[1]] == array[triple[2]]:
#             return array[triple[0]]
#     return None

triples0 = [[1, 2], [3, 6]]
triples4 = [[3, 5], [1, 7], [0, 8], [2, 6]]
triples8 = [[6, 7], [2, 5]]

def check_3_in_row(array):
    if array[0] != N:
        for triple in triples0:
            if array[0] == array[triple[0]] == array[triple[1]]:
                return array[0]
    if array[4] != N:
        for triple in triples4:
            if array[4] == array[triple[0]] == array[triple[1]]:
                return array[4]
    if array[8] != N:
        for triple in triples8:
            if array[8] == array[triple[0]] == array[triple[1]]:
                return array[8]
    return N


def get_board_symbol(value):
    return "X" if value == P1 else \
        ("O" if value == P2 else "_")


class Board(ABC):

    def __init__(self):
        self.previous = None
        self.numFilled = 0

    def __getitem__(self, args):
        return self.get(args)

    def __iadd__(self, args):
        self.previous = args
        self.numFilled += 1
        self.set_move(args)
        return self

    def __ilshift__(self, args):
        self.set_move(args)
        self.previous = args
        self.numFilled += 1
        return self

    def __len__(self):
        return self.numFilled

    @abstractmethod
    def get(self, args):
        pass

    @abstractmethod
    def set_move(self, args):
        pass

    @abstractmethod
    def print(self):
        pass

class Quadrants(Board):

    def __init__(self, other=None):
        super().__init__()
        if other is None:
            self.board = [N, N, N, N, N, N, N, N, N]
            self.remaining = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            b = other.board
            self.board =  [b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8]]
            self.remaining =  other.remaining[:]
            self.numFilled = other.numFilled

    def get(self, quadrant):
        return self.board[quadrant]

    # def get_quadrant(self, quadrant):
    #     return self.board[quadrant]

    def set_move(self, args):
        quadrant, player = args
        # print(args, self.board)
        self.board[quadrant] = player
        # try:
        self.remaining.remove(quadrant)
        # except Exception:
        #     self.print()
        #     print(self.remaining)
        #     print(self.previous)
        #     print(quadrant, player)
        #     raise

    def print(self):
        for a in range(0, 3):
            for b in range(0, 3):
                print(get_board_symbol(self.board[3*a+b]), end="")
            print("")

class Board2D(Board):
    def __init__(self, other=None):
        super().__init__()
        if other is None:
            self.board = [[N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N],
                          [N, N, N, N, N, N, N, N, N]]
            self.remaining = [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8]]
        else:
            b = other.board
            self.board = [[b[0][0], b[0][1], b[0][2], b[0][3], b[0][4], b[0][5], b[0][6], b[0][7], b[0][8]],
                          [b[1][0], b[1][1], b[1][2], b[1][3], b[1][4], b[1][5], b[1][6], b[1][7], b[1][8]],
                          [b[2][0], b[2][1], b[2][2], b[2][3], b[2][4], b[2][5], b[2][6], b[2][7], b[2][8]],
                          [b[3][0], b[3][1], b[3][2], b[3][3], b[3][4], b[3][5], b[3][6], b[3][7], b[3][8]],
                          [b[4][0], b[4][1], b[4][2], b[4][3], b[4][4], b[4][5], b[4][6], b[4][7], b[4][8]],
                          [b[5][0], b[5][1], b[5][2], b[5][3], b[5][4], b[5][5], b[5][6], b[5][7], b[5][8]],
                          [b[6][0], b[6][1], b[6][2], b[6][3], b[6][4], b[6][5], b[6][6], b[6][7], b[6][8]],
                          [b[7][0], b[7][1], b[7][2], b[7][3], b[7][4], b[7][5], b[7][6], b[7][7], b[7][8]],
                          [b[8][0], b[8][1], b[8][2], b[8][3], b[8][4], b[8][5], b[8][6], b[8][7], b[8][8]]]
            b = other.remaining
            self.remaining = [b[0][:], b[1][:], b[2][:], b[3][:], b[4][:], b[5][:], b[6][:], b[7][:], b[8][:]]
            self.numFilled = other.numFilled

    def get(self, args):
        return self.board[args]

    def set_move(self, args):
        globalMove, localMove, player = args
        self.board[globalMove][localMove] = player
        self.remaining[globalMove].remove(localMove)

    def print(self):
        for a in range(0, 3):
            for b in range(0, 3):
                for c in range(0, 3):
                    for d in range(0, 3):
                        print(get_board_symbol(self.board[3*a+c][3*b+d]), end="")
                    print("  ", end="")
                print("")
            print("")
