import sys
sys.path.append("../../")

from UTTT.play import play_UTTT
from APVMCTS import *
import random
from Model import *
from Environment import *

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Testing on:  ", device)

model = UTTT_Model("./Attempts/supervised5/most_recent_uttt_model").to(device)

numP1Wins = 0
numP2Wins = 0
numTies = 0

def getDQNMove(node, verbose=True, iterations=8000):
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

    move = getMove(node, model, device, iterations=iterations)
    
    if verbose:
        end = current_time_milli()
        if node.children is not None:
            for child in node.children:
                print(child.value, child.totalAction, child.numVisits, child.priorProbability)
            best_child = getChildVisitedMost(node)
            print("Search Space Size:  {0}".format(best_child.parent.numVisits))
            print(f"g:   {move[0]}      l:   {move[1]}")
            print(f"v:   {best_child.getValue()}      n:   {best_child.numVisits}")
            print(f"confidence:   {best_child.getConfidence()}")
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
            np.multiply(rewards, legal_moves, rewards)
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

def create_APVMCTS_node():
    return APVMCTS_Node(0)

if __name__ == "__main__":
    print(model.state_dict())
    # play_UTTT(P2_move=getDQNMove, create_node=create_APVMCTS_node)

