import sys
sys.path.append("../../")

from UTTT import *
from UTTT.MCTS import *
import random
from Model import *

device = torch.device("cpu") # "cuda:0" if torch.cuda.is_available() else 
print("Testing on:  ", device)

model = UTTT_Model("./Attempts/supervised3/most_recent_uttt_model").to(device)

numP1Wins = 0
numP2Wins = 0
numTies = 0

def DQN_Policy(move, quadrants, board, length):
    legal_moves = getLegalMovesField(quadrants, board, move)
    rewards = model.predict(transform_board(board), device)
    np.multiply(rewards+1, legal_moves, rewards)
    next_move = unflatten_move(argmax(rewards))

    move[0] = next_move[0]
    move[1] = next_move[1]

def DQN_simulation(quadrants, board, winner, move, player, length):
    # global numP1Wins
    # global numP2Wins
    # global numTies
    
    winner, time_step = simulation(quadrants, board, winner, move, player, length, DQN_Policy)
    # if winner == P1:
    #     numP1Wins += 1
    # elif winner == P2:
    #     numP2Wins += 1
    # else:
    #     numTies += 1
    return winner # (1 if winner == player else -1)*(q.gamma**time_step)

def getDQNMove(node, verbose=True, iterations=400):
    if verbose:
        printBoard(node.buildBoard2D(), node.buildQuadrant())
        print("Computer is thinking...")
        start = current_time_milli()

    # board = node.buildBoard2D()
    # quadrants = node.buildQuadrant()

    # legal_moves = getLegalMovesField(quadrants, board, node.getMove())
    # rewards = model.predict(transform_board(board), device)+1
    # np.multiply(rewards, legal_moves, rewards)

    # move = argmax(rewards)
    # move = unflatten_move(move)

    move = getMove(node, iterations=iterations, simulation=DQN_simulation)
    
    if verbose:
        end = current_time_milli()
        print("Search Space Size:  {0}".format(node.getNumVisits()))
        print(f"g:   {move[0]}      l:   {move[1]}")
        print(f"w:   {node.numWins}      v:   {node.numVisits}")
        print(f"confidence:   {node.getConfidence()}")
        print(f"time:         {(end-start)/1000.0} seconds")
        # print("numP1Wins: ", str(numP1Wins).ljust(5), 
        #      "numP2Wins: ", str(numP2Wins).ljust(5), 
        #      "numTies: ", str(numTies).ljust(5))

    return move

def test_win_ratio():
    numP1Wins = 0
    numP2Wins = 0
    numTies = 0
    env = UTTT_Environment()
    for i in range(1000):
        observation = env.reset()
        observation, reward, done, info = env.step(unflatten_move(np.random.randint(81)))
        observation, reward, done, info = env.step(get_second_move(*env.previousMove))

        done = False
        while not done:
            
            legal_moves = getLegalMovesField(env.quadrants, env.board, env.previousMove)
            rewards = model.predict(transform_board(observation), device)
            np.multiply(rewards+1, legal_moves, rewards)
            action = unflatten_move(argmax(rewards))

            observation, reward, done, info = env.step(action)

        if env.winner == P1:
            numP1Wins += 1
        elif env.winner == P2:
            numP2Wins += 1
        else:
            numTies += 1

        print("\rGame: ", str(i).ljust(5),
             "numP1Wins: ", str(numP1Wins).ljust(5), 
             "numP2Wins: ", str(numP2Wins).ljust(5), 
             "numTies: ", str(numTies).ljust(5), end="")

    print()
    # numP1Wins:  461   numP2Wins:  361   numTies:  178

if __name__ == "__main__":
    play_UTTT(P2_move=getDQNMove)

