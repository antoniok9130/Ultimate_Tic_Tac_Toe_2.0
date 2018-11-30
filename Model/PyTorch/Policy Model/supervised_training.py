
import platform
import sys
if platform.platform() == "Windows":
    sys.path.append("..\\..\\..\\")
else:
    sys.path.append("../../../")

    
import subprocess as sp

import numpy as np
from numba import jit
import torch
from math import ceil

from UTTT import *
from random import shuffle
from Policy_Model import *


# quadrant_rotations = (2, 5, 0, 7, 4, 1, 8, 3, 6)

# @jit(cache=True, nopython=True)
# def rotate_quadrants(move, n=0):
#     g, l = move
#     for _ in range(n):
#         g = quadrant_rotations[g]
#         l = quadrant_rotations[l]
    
#     return g, l


def traverse_moves(moves, permute=False):
    features = []

    board = np.zeros((9, 9))
    # quadrants = np.zeros((3, 3))

    length = 0
    player = N
    for i in range(len(moves)-1):

        player = P2 if player == P1 else P1

        g, l = moves[i]
        board[g][l] = player
        # if check3InRowAt(board[g], l):
        #     quadrants[int(g//3)][g%3] = player
        length += 1

        g, l = moves[i+1]
        expected = np.zeros((9, 9))
        expected[g][l] = 1

        if permute:
            for k in range(4):
                expected = rotate_quadrants(moves[i+1], k)
                features.append((
                    extract_features(
                        # np.rot90(quadrants, k=k).ravel(),
                        np.rot90(board, k=k)
                    ),
                    np.rot90(expected, k=k).ravel()
                ))
                features.append((
                    extract_features(
                        # np.rot90(np.fliplr(quadrants), k=k).ravel(),
                        np.rot90(np.fliplr(board), k=k)
                    ),
                    np.rot90(np.fliplr(expected), k=k).ravel()
                ))
        else:
            features.append((extract_features(board), expected.ravel())) # quadrants.ravel(), 

    # winner = check3InRow(quadrants.ravel())

    # if winner == P1:
    #     expected = 1
    # elif winner == P2:
    #     expected = 2
    # else:
    #     expected = 0

    # return features, expected

    return features


def get_features(record, permute=False):
    return traverse_moves([(int(record[i]), int(record[i+1])) for i in range(0, len(record), 2)], permute=permute)



def get_batches(data, batch_size=32, proportion_val=0):
    shuffle(data)

    if batch_size is None:
        return [np.array(list(t)) for t in zip(*data)]
        
    training_inputs = [[]]
    training_labels = [[]]

    val_inputs = []
    val_labels = []

    for _input_, _label_ in data:
        if len(val_inputs) < len(data)*proportion_val:
            val_inputs.append(_input_)
            val_labels.append(_label_)

        else:
            if len(training_inputs[-1]) >= batch_size:
                training_inputs[-1] = np.reshape(training_inputs[-1], (-1, input_size))
                # training_inputs[-1] = np.array(training_inputs[-1])
                training_labels[-1] = np.array(training_labels[-1])
                training_inputs.append([])
                training_labels.append([])

            training_inputs[-1].append(_input_)
            training_labels[-1].append(_label_)

    training_inputs[-1] = np.reshape(training_inputs[-1], (-1, input_size))
    training_labels[-1] = np.array(training_labels[-1])
    val_inputs = np.array(val_inputs)
    val_labels = np.array(val_labels)

    return training_inputs, training_labels, val_inputs, val_labels


def train():
    test_data = []

    num_recorded_games = file_len("../Data/ValidationGames.txt")
    print("Loading Test Data...")
    with open("../Data/ValidationGames.txt") as file, ProgressBar(num_recorded_games, 50) as progress:
        records = [row.strip() for row in file]
        for record in records:
            next(progress)
            features = get_features(record)
            shuffle(features)
            test_data.extend(features)
        
        test_data = get_batches(test_data, batch_size=None)



    model_instance_directory = "../ModelInstances/policy3"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)
    sp.call(f"touch {model_instance_directory}/log.csv", shell=True)

    with open(f"{model_instance_directory}/log.csv", "w") as file:
        file.write(f"iteration,loss,accuracy\n")


    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = Predict_Model()

    with open(f"../Data/TrainingGames.txt") as file:
        games = list(set([row.strip() for row in file]))


    min_loss = 1000
    max_accuracy = -1000
    iteration = 1
    
    while True:
        shuffle(games)
        for i in range(0, len(games), 289):
            try:
                print(f"Iteration {iteration}:")
                game_set = games[i:i+289]
                if len(game_set) > 0:
                    train_data = []

                    for game in game_set:
                        features = get_features(game, permute=True)
                        train_data.append((feature, expected))
                    
                    shuffle(train_data)
                    training_inputs, training_labels, val_inputs, val_labels = get_batches(train_data)

                    model = model.to(device)

                    criterion = torch.nn.MSELoss()
                    optimizer = torch.optim.SGD(model.parameters(), lr=0.01) # , momentum=0.9

                    running_losses = 0
                    num_train_iterations = 0
                    num_epochs = 5
                    with ProgressBar(num_epochs*len(train_data), 50) as progress:
                        for epoch in range(num_epochs):
                            for training_input, training_label in zip(training_inputs, training_labels):
                                next(progress)
                                if len(training_input) > 0:
                                    input_tensor = torch.from_numpy(training_input).double().to(device)
                                    label_tensor = torch.from_numpy(training_label).double().to(device)

                                    outputs = model.forward(input_tensor)
                                    optimizer.zero_grad()
                                    loss = criterion(outputs, label_tensor)
                                    loss.backward()
                                    optimizer.step()
                                    running_losses[i] += loss.item()

                                    num_train_iterations[i] += 1


                    model = model.cpu()

                    correct = [0.0 for l in lengths]
                    num_accuracy_iterations = [0 for l in lengths]
                    with torch.no_grad():
                        for i, test_data_point in enumerate(test_data):
                            if len(test_data_point) > 0:
                                test_input, test_label = test_data_point

                                if len(test_input) > 0:
                                    input_tensor = torch.from_numpy(test_input)
                                    label_tensor = torch.from_numpy(test_label).long()

                                    outputs = model.forward(input_tensor, i*15)
                                    _, predicted = torch.max(outputs.data, 1)
                                    correct[i] += (predicted == label_tensor).sum().item()

                                    num_accuracy_iterations[i] += len(test_input)


                    average_loss = sum(l/i for l, i in zip(running_losses, num_train_iterations))/len(lengths)
                    if average_loss < min_loss:
                        model.save_weights(f"{model_instance_directory}/predict_model_min_average_loss")
                        min_loss = average_loss

                    average_accuracy = sum(c/i for c, i in zip(correct, num_accuracy_iterations))/len(lengths)
                    if average_accuracy > max_accuracy:
                        model.save_weights(f"{model_instance_directory}/predict_model_max_average_accuracy")
                        max_accuracy = average_accuracy
                    
                    model.save_weights(f"{model_instance_directory}/predict_model_most_recent")

                    with open(f"{model_instance_directory}/log.csv", "a") as file:
                        file.write("{},{},{}\n".format(
                            iteration,
                            ','.join([str(l/i) for l, i in zip(running_losses, num_train_iterations)]),
                            ','.join([str(c/i) for c, i in zip(correct, num_accuracy_iterations)])
                        ))

                iteration += 1

            except:
                pass
        
        model.save_weights(f"{model_instance_directory}/predict_model_{iteration}")



if __name__ == "__main__":

    # train()

    # num_records = file_len("../../../Game/C++/MCTS_V2.5/record20.txt")
    # print("Loading Data...")
    # data = []
    # with open("../../../Game/C++/MCTS_V2.5/record20.txt") as file, ProgressBar(num_records, 50) as progress:
    #     records = [row.strip() for row in file]
    #     for record in records:
    #         next(progress)
    #         data.append(get_features(record))
            

