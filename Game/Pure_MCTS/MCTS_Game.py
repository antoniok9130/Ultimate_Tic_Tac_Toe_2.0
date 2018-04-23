import datetime
from random import SystemRandom

from Game.Pure_MCTS.Boards import check_3_in_row, P1, P2, N, Board2D, Quadrants, T
from Game.Pure_MCTS.MCTS_Node import MCTS_Node

def getMove(node, time=2):
    calculation_time = datetime.timedelta(seconds=time)
    # i = 0
    start = datetime.datetime.utcnow()
    while datetime.datetime.utcnow() - start < calculation_time:
        select(node)
        # i += 1
    print(node.numWins, "/", node.numVisits)
    return max_visit_child(node)

def max_visit_child(node):
    max_visits = 0
    max_child = []
    for child in node.children:
        if child.numVisits >= max_visits:
            if child.numVisits > max_visits:
                max_visits = child.numVisits
                max_child.clear()
            max_child.append(child)
    return SystemRandom().choice(max_child)

def max_uct_child(node):
    highest_UCT = 0
    max_child = []
    for child in node.children:
        if child.UCT >= highest_UCT:
            if child.UCT > highest_UCT:
                highest_UCT = child.UCT
                max_child.clear()
            max_child.append(child)
    return SystemRandom().choice(max_child)

def select(node):
    if node.children is None:
        node.init()
        if node.winner != N:
            backpropogate(node, node.winner)
        elif node.numVisits == 0:
            winner = run_simulation(node)
            backpropogate(node, winner)
        else:
            expand(node)
    else:
        select(max_uct_child(node))

def expand(node):
    if node.children is None:
        node.children = []
        globalMoves = []
        if node.localMove is not None and node.quadrants[node.localMove] == N:
            globalMoves.append(node.localMove)
        else:
            globalMoves.extend(node.quadrants.remaining)

        for globalMove in globalMoves:
            for localMove in node.board.remaining[globalMove]:
                node.children.append(MCTS_Node(globalMove, localMove, node, False))

        random_child = SystemRandom().choice(node.children)
        winner = run_simulation(random_child)
        backpropogate(random_child, winner)


def run_simulation(node):
    node.init()
    board = Board2D(node.board)
    quadrants = Quadrants(node.quadrants)
    localMove = node.localMove
    winner = node.winner
    while winner == N:
        if localMove is not None and quadrants[localMove] == N:
            globalMove = localMove
            # print("derived", localMove, quadrants[localMove], quadrants.board, quadrants.remaining)
        else:
            globalMove = SystemRandom().choice(quadrants.remaining)

        localMove = SystemRandom().choice(board.remaining[globalMove])
        board <<= (globalMove, localMove, P1 if len(board)%2 == 0 else P2)

        filled = check_3_in_row(board[globalMove])
        if filled != N:
            quadrants <<= (globalMove, filled)
            if len(quadrants) > 2:
                winner = check_3_in_row(quadrants)
                if winner == N and not quadrants.remaining:
                    return T
        elif not board.remaining[globalMove]:
            quadrants <<= (globalMove, T)
            if not quadrants.remaining:
                return T
    return winner

def backpropogate(node, winner):
    if node.player == winner:
        node.numWins += 1
    node.numVisits += 1

    if node.parent is not None:
        backpropogate(node.parent, winner)

    node.updateUCT()
