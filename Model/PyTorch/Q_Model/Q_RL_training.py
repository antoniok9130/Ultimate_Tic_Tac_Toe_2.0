
import platform
import sys
if platform.platform() == "Windows":
    sys.path.append("..\\..\\..\\")
else:
    sys.path.append("../../../")

    
import subprocess as sp
from math import inf

import numpy as np
from numba import jit
import torch
from math import ceil

from UTTT import *
from random import shuffle, sample
from Q_Model import *


# quadrant_rotations = (2, 5, 0, 7, 4, 1, 8, 3, 6)

# @jit(cache=True, nopython=True)
# def rotate_quadrants(move, n=0):
#     g, l = move
#     for _ in range(n):
#         g = quadrant_rotations[g]
#         l = quadrant_rotations[l]
    
#     return g, l

# path_to_transitions = "../ModelInstances/Q1/transitions.txt"
# sp.call(f"touch {path_to_transitions}", shell=True)
max_number_of_transitions = 55000


# def transition_to_str(board, action, rewards):
#     return "{}|{}|{}".format(
#             "".join("".join([str(int(m)) for m in quadrant]) for quadrant in board),
#             "".join(str(a) for a in action),
#             ",".join(str(r) for r in rewards))


# def add_to_transitions(board, action, rewards):
#     with open(path_to_transitions, "a") as transitions:
#         transitions.write(transition_to_str(board, action, rewards)+"\n")

# def write_transitions(transitions):
#     with open(path_to_transitions, "w") as file:
#         file.write("\n".join(transition_to_str(t[0], t[1], t[2]) for t in transitions))

# def read_from_transitions():
#     with open(path_to_transitions) as file:
#         lines = file.read().strip().split("\n")[-max_number_of_transitions:]

#     transitions = []
#     for line in lines:
#         parts = line.split("|")
#         transitions.append((
#             np.reshape(np.array([int(m) for m in list(parts[0])]), (9, 9)),
#             tuple(int(a) for a in list(parts[1])),
#             np.array([float(r) for r in parts[2].split(",")])
#         ))

#     return transitions


def transition_to_features(board, reward, permute=False):
    features = []

    feature = extract_features(board)
    reward = np.reshape(reward, (9, 9))

    if permute:
        for k in range(4):
            features.append((
                np.rot90(feature, k=k, axes=(1,2)),
                np.rot90(reward, k=k).ravel()
            ))
            features.append((
                np.rot90(np.fliplr(feature), k=k, axes=(1,2)),
                np.rot90(np.fliplr(reward), k=k).ravel()
            ))
    else:
        features.append((feature, reward.ravel()))

    return features


def train():
    transitions = []

    def add_to_transitions(board, action, reward, terminal):
        transitions.append((board, action, reward, terminal))
        if len(transitions) > max_number_of_transitions:
            transitions.pop(0)


    model_instance_directory = "../ModelInstances/Q1"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)
    sp.call(f"touch {model_instance_directory}/log.csv", shell=True)

    with open(f"{model_instance_directory}/log.csv", "w") as file:
        file.write(f"iteration,loss\n")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = Q_Model()

    min_loss = inf
    explore_prob = 0.02
    iteration = 1
    
    criterion = torch.nn.MSELoss()

    while True:
        for i in range(9):
            for j in range(9):
                try:
                    print("\nIteration:  ", iteration)
                    start = current_time_milli()

                    first_move = (i, j)
                    second_move = get_second_move(i, j)

                    board = np.zeros((9, 9))
                    quadrants = np.zeros(9)
                    num_remaining_board = [9 for i in range(9)]
                    num_remaining_quadrant = 9
                    player = P1
                    winner = N
                    length = 2

                    board[i][j] = P1
                    num_remaining_board[i] -= 1
                    board[second_move[0]][second_move[1]] = P2
                    num_remaining_board[second_move[0]] -= 1
                    previousMove = second_move

                    while winner == N: # no winner
                        legal_moves = getLegalMovesField(quadrants, board, previousMove)
                        rewards = model.predict(extract_features(board))[0]
                        np.multiply(rewards, legal_moves, rewards)

                        if np.random.random() < explore_prob:
                            move = random.choice(legal_moves)
                        else:
                            move = np.random.choice(np.flatnonzero(rewards == rewards.max()))

                        g = int(move//9)
                        l = int(move%9)
                        board[g][l] = player
                        num_remaining_board[g] -= 1
                        previousMove = (g, l)
                        length += 1        

                        if check3InRowAt(board[g], l):
                            quadrants[g] = player
                            num_remaining_quadrant -= 1
                        elif num_remaining_board[g] < 1:
                            quadrants[g] = T
                            num_remaining_quadrant -= 1
                        
                        if check3InRowAt(quadrants, g):
                            winner = player
                        elif num_remaining_quadrant < 1:
                            winner = T
                            
                        reward = compute_reward(quadrants, board, winner, previousMove, player, length, model)
                        rewards[int(move)] = reward

                        player = P2 if player == P1 else P1

                        add_to_transitions(board.copy(), previousMove, rewards, winner != N)

                        # train
                        sample_transitions = sample(transitions, min(len(transitions), 32))
                        features = []
                        for transition in sample_transitions:
                            features.extend(transition_to_features(transition[0], transition[2], permute=True))

                        shuffle(features)

                        model = model.to(device)
                        optimizer = torch.optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)
                        running_loss = 0
                        num_iterations = 0
                        for sample_state, sample_rewards in features:
                            input_tensor = torch.from_numpy(np.reshape(sample_state, (-1, 2, 9, 9)).copy()).double().to(device)
                            label_tensor = torch.from_numpy(np.reshape(sample_rewards, (1, 81)).copy()).double().to(device)
                        
                            outputs = model.forward(input_tensor)
                            optimizer.zero_grad()
                            loss = criterion(outputs, label_tensor)
                            loss.backward()
                            optimizer.step()
                            running_loss += loss.item()

                            num_iterations += 1

                        loss = running_loss/num_iterations
                        with open(f"{model_instance_directory}/log.csv", "w") as file:
                            file.write(f"{iteration},{loss}\n")

                        model = model.cpu()

                        if loss < min_loss:
                            model.save_weights(f"{model_instance_directory}/q_model_min_loss")
                            min_loss = loss

                        model.save_weights(f"{model_instance_directory}/pq_model_most_recent")

                        end = current_time_milli()
                        print(f"Loss:             {loss}")
                        print(f"Num Transitions:  {len(transitions)}")
                        print(f"Time:             {(end-start)/1000.0}")

                        iteration += 1

                except:
                    pass



if __name__ == "__main__":

    # board = np.zeros((9, 9))
    # board[0][2] = 1
    # board[3][7] = 2

    # rewards = np.zeros(81)
    # rewards[56] = 1.345

    # add_to_dataset(board, (6, 2), rewards)

    # print(read_from_transitions())

    # transition_to_features(np.random.randint(3, size=(9, 9)), np.random.randint(2, size=81), permute=True)

    # start = current_time_milli()

    # for i in range(55000):
    #     transition_to_features(np.random.randint(3, size=(9, 9)), np.random.randint(2, size=81), permute=True)

    # end = current_time_milli()
    # print((end-start)/1000.0)

    train()

    # num_records = file_len("../../../Game/C++/MCTS_V2.5/record20.txt")
    # print("Loading Data...")
    # data = []
    # with open("../../../Game/C++/MCTS_V2.5/record20.txt") as file, ProgressBar(num_records, 50) as progress:
    #     records = [row.strip() for row in file]
    #     for record in records:
    #         next(progress)
    #         data.append(get_features(record))
            

