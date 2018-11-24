
import platform
import sys
if platform.platform() == "Windows":
    sys.path.append("..\\..\\..\\")
else:
    sys.path.append("../../../")

    
import subprocess as sp

import numpy as np
import torch
from math import ceil

from UTTT import *
from random import shuffle
from Predict_Model import *


def traverse_moves(moves, permute=False):
    features = []

    board = np.zeros((9, 9))
    quadrants = np.zeros((3, 3))

    length = 0
    player = N
    for g, l in moves:

        player = P2 if player == P1 else P1

        board[g][l] = player
        if check3InRowAt(board[g], l):
            quadrants[int(g//3)][g%3] = player
        length += 1

        if permute:
            for k in range(4):
                features.append((
                    extract_features(
                        np.rot90(quadrants, k=k).ravel(),
                        np.rot90(board, k=k)
                    ),
                    length
                ))
                features.append((
                    extract_features(
                        np.rot90(np.fliplr(quadrants), k=k).ravel(),
                        np.rot90(np.fliplr(board), k=k)
                    ),
                    length
                ))
        else:
            features.append((extract_features(quadrants.ravel(), board), length))

    winner = check3InRow(quadrants.ravel())

    if winner == P1:
        expected = 1
    elif winner == P2:
        expected = 2
    else:
        expected = 0

    return features, expected


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
    lengths = ["0_15", "15_30", "30_45", "45_60", "60_"]
    length_interval = 15

    test_data = [[] for l in lengths]

    num_recorded_games = file_len("../Data/ValidationGames.txt")
    print("Loading Test Data...")
    with open("../Data/ValidationGames.txt") as file, ProgressBar(num_recorded_games, 50) as progress:
        records = [row.strip() for row in file]
        for record in records:
            next(progress)
            features, expected = get_features(record)
            shuffle(features)
            for feature, length in features:            
                test_data[min(int(length//length_interval), len(lengths)-1)].append((feature, expected))
        
        for i in range(len(test_data)):
            test_data[i] = get_batches(test_data[i], batch_size=None)



    model_instance_directory = "../ModelInstances/predict7"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)
    sp.call(f"touch {model_instance_directory}/log.csv", shell=True)

    with open(f"{model_instance_directory}/log.csv", "w") as file:
        file.write(f"iteration,{f'loss__{length}' for length in lengths},{f'accuracy__{length}' for length in lengths}\n")


    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = Predict_Model()

    games = []
    for i in range(20, 23):
        with open(f"../../../Game/C++/MCTS_V2.5/record{i}.txt") as file:
            games.extend([row.strip() for row in file])

    games = list(set(games))


    min_loss = 1000
    max_accuracy = -1000
    iteration = 1
    
    while True:
        shuffle(games)
        for i in range(0, len(games), 289):
            print(f"Iteration {iteration}:")
            game_set = games[i:i+289]
            train_data = [[] for l in lengths]

            for game in game_set:
                features, expected = get_features(game, permute=True)
                shuffle(features)
                for feature, length in features:            
                    train_data[min(int(length//length_interval), len(lengths)-1)].append((feature, expected))
            
            for i in range(len(train_data)):
                train_data[i] = get_batches(train_data[i])

            model = model.to(device)

            criterion = torch.nn.CrossEntropyLoss()
            optimizer = torch.optim.SGD(model.parameters(), lr=0.01) # , momentum=0.9

            running_losses = [0.0 for l in lengths]
            num_train_iterations = [0 for l in lengths]
            num_epochs = 5
            with ProgressBar(num_epochs*len(train_data)*sum(len(x[0]) for x in train_data), 50) as progress:
                for epoch in range(num_epochs):
                    for i, data in enumerate(train_data):
                        training_inputs, training_labels, val_inputs, val_labels = data
                        for training_input, training_label in zip(training_inputs, training_labels):
                            next(progress)
                            if len(training_input) > 0:
                                input_tensor = torch.from_numpy(training_input).to(device)
                                label_tensor = torch.from_numpy(training_label).long().to(device)

                                outputs = model.forward(input_tensor, i*15)
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
                    ','.join(l/i for l, i in zip(running_losses, num_train_iterations)),
                    ','.join(c/i for c, i in zip(correct, num_accuracy_iterations))
                ))

            iteration += 1



if __name__ == "__main__":

    train()

    # num_records = file_len("../../../Game/C++/MCTS_V2.5/record20.txt")
    # print("Loading Data...")
    # data = []
    # with open("../../../Game/C++/MCTS_V2.5/record20.txt") as file, ProgressBar(num_records, 50) as progress:
    #     records = [row.strip() for row in file]
    #     for record in records:
    #         next(progress)
    #         data.append(get_features(record))
            

