from copy import deepcopy
from random import randint, SystemRandom

triples = [[0, 1, 2],
           [6, 7, 8],
           [0, 3, 6],
           [2, 5, 8],
           [3, 4, 5],
           [1, 4, 7],
           [0, 4, 8],
           [2, 4, 6]]


class UTTT:
    def __init__(self, other=None):
        if other == None or not isinstance(other, UTTT):
            self.winner = 0

            self.boards = {}
            self.board = Board2D()
            self.add_boards(board=self.board)

            self.board2dLeft = [[i for i in range(9)] for _ in range(9)]

            self.grid3by3 = [0 for _ in range(9)]
            self.grid3by3Left = [i for i in range(9)]

            self.moves = []
            self.gameLength = 0
        else:
            self.copy_other(other)

    def copy_other(self, other):
        self.winner = other.winner

        self.boards = {}
        self.board = deepcopy(other.board)
        self.add_boards(board=self.board)

        self.board2dLeft = deepcopy(other.board2dLeft)

        self.grid3by3 = deepcopy(other.grid3by3)
        self.grid3by3Left = deepcopy(other.grid3by3Left)

        self.moves = deepcopy(other.moves)
        self.gameLength = other.gameLength

    def __checkFilled(self):
        globalMove = self.moves[-1][0]

        filled = 0
        for triple in triples:
            state = self.board.get(globalMove, triple[0]) + \
                    self.board.get(globalMove, triple[1]) + \
                    self.board.get(globalMove, triple[2])
            if state == 3:
                filled = 2
                break
            elif state == -3:
                filled = 1
                break

        if filled != 0:
            self.grid3by3[globalMove] = filled
            self.grid3by3Left.remove(globalMove)
            self.__checkWinner()
        elif not self.board2dLeft[globalMove]:
            self.grid3by3[globalMove] = 3
            self.grid3by3Left.remove(globalMove)
            self.__checkWinner()

        self.gameLength += 1

    def __checkWinner(self):
        if self.winner != 0:
            return
        for triple in triples:
            state = self.grid3by3[triple[0]] * \
                    self.grid3by3[triple[1]] * \
                    self.grid3by3[triple[2]]
            if state == 8:
                self.__setWinner(2)
                return
            elif state == 1:
                self.__setWinner(1)
                return
        if not self.grid3by3Left:
            self.__setWinner(3)

    def __setWinner(self, winner):
        self.winner = winner

    def runSimulation(self):
        while self.addRandom():
            pass

    def add_move(self, globalMove, localMove):
        if self.winner != 0:
            return False
        self.moves.append([globalMove, localMove, 2*(self.gameLength % 2)-1])
        self.board2dLeft[globalMove].remove(localMove)

        args = (globalMove, localMove, self.moves[-1][2])
        for board in self.boards:
            self.boards[board].set_move(*args)

        self.__checkFilled()
        return True

    def addRandom(self):
        if self.winner != 0:
            return False
        globalMove = (randint(0, 8) if self.gameLength == 0
                      else (self.moves[-1][1] if self.grid3by3[self.moves[-1][1]] == 0
                            else SystemRandom().choice(self.grid3by3Left)))
        localMove = SystemRandom().choice(self.board2dLeft[globalMove])

        return self.add_move(globalMove, localMove)

    def add_boards(self, **kwargs):
        for key in kwargs:
            self.boards[key] = kwargs[key]


    def print(self, board="board"):
        if board in self.boards:
            self.boards[board].print()

def get_board_symbol(value):
    return "X" if value == -1 else \
        ("O" if value == 1 else "_")

class Board1D:
    def __init__(self):
        self.board = [0 for _ in range(81)]

    def get(self, globalMove, localMove):
        return self.board[9 * globalMove + localMove]

    def set_move(self, globalMove, localMove, player):
        self.board[9 * globalMove + localMove] = player

    def print(self):
        for a in range(0, 3):
            for b in range(0, 3):
                for c in range(0, 3):
                    for d in range(0, 3):
                        print(get_board_symbol(self.board[9*(3*a+c)+3*b+d]), end="")
                    print("  ", end="")
                print("")
            print("")


class Board2D:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def get(self, globalMove, localMove):
        return self.board[globalMove][localMove]

    def set_move(self, globalMove, localMove, player):
        self.board[globalMove][localMove] = player

    def print(self):
        for a in range(0, 3):
            for b in range(0, 3):
                for c in range(0, 3):
                    for d in range(0, 3):
                        print(get_board_symbol(self.board[3*a+c][3*b+d]), end="")
                    print("  ", end="")
                print("")
            print("")


class Board2Drows:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def get(self, globalMove, localMove):
        return self.board[3 * (globalMove // 3) + (localMove // 3)][3 * (globalMove % 3) + (localMove % 3)]

    def set_move(self, globalMove, localMove, player):
        self.board[3 * (globalMove // 3) + (localMove // 3)][3 * (globalMove % 3) + (localMove % 3)] = player

    def print(self):
        for a in range(9):
            for b in range(9):
                print(get_board_symbol(self.board[a][b]), end="")
                if b == 2 or b == 5:
                    print("  ", end="")
            print()
            if a == 2 or a == 5 or a == 8:
                print("")
