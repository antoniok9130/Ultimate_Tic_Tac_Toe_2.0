import datetime

from Game.Pure_MCTS.Boards import N
from Game.Pure_MCTS.MCTS_Node import MCTS_Node
from Game.Pure_MCTS.MCTS_Game import getMove

def play():
    game = MCTS_Node()
    while game.winner == N:
        game.quadrants.print()
        print()
        game.board.print()
        move = input("Enter Move:  ").split(" ")
        if len(move) == 2:
            globalMove = int(move[0])
            localMove = int(move[1])
            if game.is_legal(globalMove, localMove):
                game = MCTS_Node(globalMove, localMove, game)
                game.board.print()
                if game.winner == N:
                    start = datetime.datetime.utcnow()
                    move = getMove(game)
                    end = datetime.datetime.utcnow()
                    print("G:", move.globalMove, "     L: ", move.localMove)
                    print("W:", move.numWins, "     V: ", move.numVisits)
                    print(end - start)
                    game.visited_children = [move]
                    game = move

    print(game.winner, "is the winner!")

if __name__ == "__main__":
    play()
    # l1 = [1, 2, 3]
    # l2 = [l1[0], l1[1], l1[2]]
    # print(l1, l2)
    # l1[1] = 4
    # print(l1, l2)