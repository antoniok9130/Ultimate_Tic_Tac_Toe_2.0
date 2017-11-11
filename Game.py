from random import randint, SystemRandom

triples = [[0, 1, 2],
           [6, 7, 8],
           [0, 3, 6],
           [2, 5, 8],
           [3, 4, 5],
           [1, 4, 7],
           [0, 4, 8],
           [2, 4, 6]]


class Game:
    def __init__(self):
        self.winner = 0

        self.board1d = [0 for _ in range(81)]
        self.board2d = [[0 for _ in range(9)] for _ in range(9)]
        self.board2drows = [[0 for _ in range(9)] for _ in range(9)]

        self.board2dLeft = [[i for i in range(9)] for _ in range(9)]

        self.grid3by3 = [0 for _ in range(9)]
        self.grid3by3Left = [i for i in range(9)]

        self.moves = []
        self.gameLength = 0

    def __checkFilled(self):
        globalMove = self.moves[-1][0]

        filled = 0
        for triple in triples:
            state = self.board2d[globalMove][triple[0]] * \
                    self.board2d[globalMove][triple[1]] * \
                    self.board2d[globalMove][triple[2]]
            if state == 8:
                filled = 2
                break
            elif state == 1:
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
        while self.winner == 0:
            self.addRandom()

    def addMove(self, globalMove, localMove):
        if self.winner != 0:
            return False
        self.moves.append([globalMove, localMove, self.gameLength%2+1])
        self.board2dLeft[globalMove].remove(localMove)

        self.board1d[9*globalMove+localMove] = self.moves[-1][2]
        self.board2d[globalMove][localMove] = self.moves[-1][2]
        self.board2drows[3*(globalMove//3)+(localMove//3)][3*(globalMove%3)+(localMove%3)] = self.moves[-1][2]

        self.__checkFilled()
        return True

    def addRandom(self):
        if self.winner != 0:
            return False
        globalMove = (randint(0, 8) if self.gameLength == 0
                      else (self.moves[-1][1] if self.grid3by3[self.moves[-1][1]] == 0
                            else SystemRandom().choice(self.grid3by3Left)))
        localMove = SystemRandom().choice(self.board2dLeft[globalMove])

        return self.addMove(globalMove, localMove)

    def print(self):
        for a in range(9):
            for b in range(9):
                print(self.board2drows[a][b], end="")
                if b == 2 or b == 5:
                    print("  ", end="")
            print()
            if a == 2 or a == 5 or a == 8:
                print("")



g = Game()
g.runSimulation()
g.print()

print(g.winner)
