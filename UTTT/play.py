
from .MCTS import *

def getHumanMove(node):
    while True:
        print()
        printBoard(node.buildBoard2D(), node.buildQuadrant())
        move = [int(m) for m in list(input("Enter Move:  ").replace(" ", ""))]
        if len(move) == 1:
            if node.move is not None:
                move = [node.move[1], move[0]]
            else:
                print("Invalid Move:  Need to enter quadrant then move")
                continue

        elif len(move) != 2:
            print("Invalid Move:  ", move)
            continue

        
        if node.isLegal(move):
            return move

        print("Illegal Move:  ", move)
        print("Current Quadrant: ", node.nextQuadrant)


def getAIMove(node, verbose=True, iterations=4800, simulation=randomSimulation):
    if verbose:
        printBoard(node.buildBoard2D(), node.buildQuadrant())
        print("Computer is thinking...")
        start = current_time_milli()

    move = getMove(node, iterations=iterations, simulation=simulation)

    if verbose:
        end = current_time_milli()
        print("Search Space Size:  {0}".format(node.getNumVisits()))
        print(f"g:   {move[0]}      l:   {move[1]}")
        print(f"w:   {node.numWins}      v:   {node.numVisits}")
        print(f"confidence:   {node.getConfidence()}")
        print(f"time:         {(end-start)/1000.0} seconds")

    return move
    
def create_MCTS_node():
    return MCTS_Node()

def play_UTTT(P1_move=getHumanMove, P2_move=getAIMove, create_node=create_MCTS_node):

    node = create_node()

    while node.winner == N:
        move = P1_move(node)
        node.setChild(move)
        node = node.getChild(0)
        
        if node.winner == N:
            move = P2_move(node)
            node.setChild(move)
            node = node.getChild(0)


    print(f"{node.winner} is the winner!")

