
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


def get_features(moves, permute=False):
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
            features.extend([(
                extract_features(
                    np.rot90(quadrants, k=k).ravel(),
                    np.rot90(board, k=k)
                ),
                length
            ) for k in range(4)])
            features.extend([(
                extract_features(
                    np.rot90(np.fliplr(quadrants), k=k).ravel(),
                    np.rot90(np.fliplr(board), k=k)
                ),
                length
            ) for k in range(4)])
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


def get_batches(data, batch_size=32, proportion_val=0.15):
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


if __name__ == "__main__":

    test_data = [
        [], # 0 - 15
        [], # 15 - 30
        [], # 30 - 45
        [], # 45 - 60
        [], # 65+
    ]

    print("Loading Test Data...")
    with open("../Data/RecordedGames.txt") as recordedGames:
        for recordedGame in recordedGames:
            recordedGame = recordedGame.strip()
            moves = [(int(recordedGame[i]), int(recordedGame[i+1])) for i in range(0, len(recordedGame), 2)]
            
            features, expected = get_features(moves)
            shuffle(features)

            for feature, length in features:            
                test_data[max(int(length//15), 4)].append((feature, expected))


    for i in range(len(test_data)):
        test_data[i] = get_batches(test_data[i], batch_size=None)

    print("Finished Loading Test Data.\n")


    model_instance_directory = "../ModelInstances/predict6"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)
    sp.call(f"touch {model_instance_directory}/log.csv", shell=True)

    with open(f"{model_instance_directory}/log.csv", "w") as file:
        file.write("iteration,duration,loss,accuracy,game,winner\n")

    min_loss = 1000
    max_accuracy = -1000
    iteration = 1

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = Predict_Model()

    with open("../ModelInstances/predict2/games.txt") as recordedGames:
        for recordedGame in recordedGames:
            recordedGame = recordedGame.strip()
            print("Iteration: ", iteration)

            train_data = [
                [], # 0 - 15
                [], # 15 - 30
                [], # 30 - 45
                [], # 45 - 60
                [], # 65+
            ]

            moves = [(int(recordedGame[i]), int(recordedGame[i+1])) for i in range(0, len(recordedGame), 2)]
            
            features, expected = get_features(moves, permute=True)
            shuffle(features)

            for feature, length in features:            
                train_data[max(int(length//15), 4)].append((feature, expected))

            for i in range(len(train_data)):
                train_data[i] = get_batches(train_data[i], batch_size=32, proportion_val=0)

            criterion = torch.nn.CrossEntropyLoss()
            optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

            model = model.to(device)

            running_loss = 0.0
            num_epochs = 5
            num_train_iterations = 0
            for epoch in range(num_epochs):
                for i, data in enumerate(train_data):
                    training_inputs, training_labels, val_inputs, val_labels = data
                    for training_input, training_label in zip(training_inputs, training_labels):
                        if len(training_input) > 0:
                            input_tensor = torch.from_numpy(training_input).to(device)
                            label_tensor = torch.from_numpy(training_label).long().to(device)

                            outputs = model.forward(input_tensor, i*15)
                            optimizer.zero_grad()
                            loss = criterion(outputs, label_tensor)
                            loss.backward()
                            optimizer.step()
                            running_loss += loss.item()

                            num_train_iterations += 1

            loss = running_loss/num_train_iterations
            print("    Loss: ", loss)

            model = model.cpu()

            correct = 0
            num_accuracy_iterations = 0
            with torch.no_grad():
                for i, test_data_point in enumerate(test_data):
                    if len(test_data_point) > 0:
                        test_input, test_label = test_data_point

                        if len(test_input) > 0:
                            input_tensor = torch.from_numpy(test_input)
                            label_tensor = torch.from_numpy(test_label).long()

                            outputs = model.forward(input_tensor, i*15)
                            _, predicted = torch.max(outputs.data, 1)
                            correct += (predicted == label_tensor).sum().item()

                            num_accuracy_iterations += len(test_input)
                    
            accuracy = correct/num_accuracy_iterations
            print("    Accuracy: ", accuracy, "\n")

            if loss < min_loss:
                model.save_weights(f"{model_instance_directory}/predict5_model_min_loss")
                min_loss = loss
            if accuracy > max_accuracy:
                model.save_weights(f"{model_instance_directory}/predict5_model_max_accuracy")
                max_accuracy = accuracy
            
            model.save_weights(f"{model_instance_directory}/predict5_model_most_recent")

            with open(f"{model_instance_directory}/log.csv", "a") as file:
                file.write(f"{iteration},,{loss},{accuracy},,\n")\

            iteration += 1
