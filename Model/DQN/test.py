import sys
sys.path.append("../../")

from UTTT import *
from UTTT.MCTS import *
import random
from Model import *

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Testing on:  ", device)

model = UTTT_Model("./Attempts/supervised2/most_recent_uttt_model").to(device)

def get_DQN_simulation_move(previousMove, quadrants, board, length):
    legal_moves = getLegalMovesField(quadrants, board, previousMove)
    rewards = model.predict(board, device)
    np.multiply(rewards, legal_moves, rewards)

    return unflatten_move(argmax(rewards))

def DQN_simulation(quadrants, board, winner, move, player, length):
    winner, time_step = simulation(quadrants, board, winner, move, player, length, get_DQN_simulation_move)

    return winner # (1 if winner == player else -1)*(q.gamma**time_step)

def getDQNMove(node, verbose=True, iterations=50):
    if verbose:
        printBoard(node.buildBoard2D(), node.buildQuadrant())
        print("Computer is thinking...")
        start = current_time_milli()

    board = node.buildBoard2D()
    quadrants = node.buildQuadrant()

    legal_moves = getLegalMovesField(quadrants, board, node.getMove())
    rewards = model.predict(board, device)+1
    np.multiply(rewards, legal_moves, rewards)

    move = argmax(rewards)
    move = unflatten_move(move)

    # move = getMove(node, iterations=iterations, simulation=DQN_simulation)

    if verbose:
        end = current_time_milli()
        # print("Search Space Size:  {0}".format(node.getNumVisits()))
        print(f"g:   {move[0]}      l:   {move[1]}")
        # print(f"w:   {node.numWins}      v:   {node.numVisits}")
        # print(f"confidence:   {node.getConfidence()}")
        print(f"time:         {(end-start)/1000.0} seconds")

    return move

if __name__ == "__main__":
    play_UTTT(P2_move=getDQNMove)
