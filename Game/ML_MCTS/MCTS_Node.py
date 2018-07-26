from math import sqrt, log

from Game.Boards import Board2D, Quadrants, check_3_in_row, P1, P2, N, T


class MCTS_Node:

    def __init__(self, globalMove=None, localMove=None, parent=None, initialize=True):
        self.globalMove = globalMove
        self.localMove = localMove
        if parent is None:
            self.winner = N
            self.parent = None
            self.board = Board2D()
            self.quadrants = Quadrants()
            self.nextQuadrant = None
            if globalMove is not None and localMove is not None:
                self.board <<= (globalMove, localMove, P1)
                self.player = P1
            else:
                self.player = N
            self.initialized = True
        else:
            self.parent = parent
            self.winner = parent.winner
            self.player = P2 if parent.player == P1 else P1
            self.board = None
            self.quadrants = None
            self.nextQuadrant = None
            self.initialized = False
            if initialize:
                if self.winner == N:
                    self.init()
                else:
                    self.board = parent.board
                    self.quadrants = parent.quadrants
                    self.initialized = True

        self.numVisits = 0
        self.numWins = 0
        self.children = None
        self.UCT = 100

    def init(self):
        if not self.initialized:
            self.board = Board2D(self.parent.board)
            self.quadrants = Quadrants(self.parent.quadrants)
            if self.globalMove is not None and self.localMove is not None:
                self.board <<= (self.globalMove, self.localMove, self.player)

                filled = check_3_in_row(self.board[self.globalMove])
                if filled != N:
                    self.quadrants <<= (self.globalMove, filled)
                    self.winner = check_3_in_row(self.quadrants)
                    if self.winner == N and not self.quadrants.remaining:
                        self.winner = T

                elif not self.board.remaining[self.globalMove]:
                    self.quadrants <<= (self.globalMove, T)
                    if not self.quadrants.remaining:
                        self.winner = T

                self.nextQuadrant = self.localMove if self.localMove in self.quadrants.remaining else None

            self.initialized = True

    def updateUCT(self):
        if self.parent is not None and self.numVisits != 0:
            self.UCT = self.numWins/self.numVisits+sqrt(2 * log(self.parent.numVisits) / self.numVisits)
	
    def is_legal(self, globalMove, localMove):
        return globalMove in self.quadrants.remaining and \
                (self.nextQuadrant is None or globalMove == self.nextQuadrant) and \
                localMove in self.board.remaining[globalMove]



