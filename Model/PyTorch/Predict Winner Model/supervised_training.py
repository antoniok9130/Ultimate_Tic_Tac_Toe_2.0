
import sys
sys.path.append("..\\..\\..\\")
import subprocess as sp

import numpy as np
import torch
from math import ceil

from UTTT import *
from random import shuffle
from Predict_Model import *

model_instance_directory = "../ModelInstances/predict4"

test_data = []

print("Loading Test Data...")
with open("../Data/RecordedGames.txt") as recordedGames:

    for recordedGame in recordedGames:
        
        game_data = []
        game = list(recordedGame.strip())

        board = np.zeros((9, 9))
        quadrants = np.zeros(9)

        i = 0
        player = N
        while i+1 < len(game):

            player = P2 if player == P1 else P1

            g = int(game[i])
            l = int(game[i+1])

            board[g][l] = player
            if check3InRowAt(board[g], l):
                quadrants[g] = player

            game_data.append(extract_features(quadrants, board))

            i += 2

        winner = check3InRow([quadrants[g] for g in range(9)])

        if winner == P1:
            expected = 1
        elif winner == P2:
            expected = 2
        else:
            expected = 0

        for features in game_data:
            test_data.append((features, expected))

shuffle(test_data)

test_inputs, test_labels = zip(*test_data)
test_inputs = np.array(test_inputs)
test_labels = np.array(test_labels)
print("Finished Loading Test Data.\n")


with open(f"{model_instance_directory}/log.csv", "w") as file:
    file.write("iteration,loss,accuracy\n")

file_name = f"../ModelInstances/predict3/games.txt"

min_loss = 1000
max_accuracy = -1000
iteration = 1

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Training on:  ", device)

model = Predict_Model()

with open(file_name) as recordedGames:
    for recordedGame in recordedGames:
        print("Iteration: ", iteration)

        data = []
        
        game_data = []
        game = list(recordedGame.strip())

        board = np.zeros((9, 9))
        quadrants = np.zeros((3, 3))

        i = 0
        player = N
        while i < len(game):

            player = P2 if player == P1 else P1

            g = int(game[i])
            l = int(game[i+1])

            board[g][l] = player
            if check3InRowAt(board[g], l):
                quadrants[int(g//3)][g%3] = player

            game_data.append((np.copy(board), np.copy(quadrants), i))

            i += 2

        winner = check3InRow([quadrants[g][l] for g in range(3) for l in range(3)])
    
        # factor = len(game) * (2 if winner == T else 1)
        for board, quadrants, length in game_data:
            # reward = 0.5+0.5*(length+1)/factor
            # penalty = 1-reward

            if winner == P1:
                expected = 1 # [reward, penalty]
            elif winner == P2:
                expected = 2 # [penalty, reward]
            else:
                expected = 0

            for k in range(4):
                data.append((
                    extract_features(
                        np.rot90(quadrants, k=k).ravel(),
                        np.rot90(board, k=k)
                    ),
                    expected
                ))
                data.append((
                    extract_features(
                        np.rot90(np.fliplr(quadrants), k=k).ravel(),
                        np.rot90(np.fliplr(board), k=k)
                    ),
                    expected
                ))


            

        shuffle(data)

        batch_size = 32
        training_inputs = [[]]
        training_labels = [[]]

        for _input_, _label_ in data:
            if len(training_inputs[-1]) >= batch_size:
                training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 900))
                # training_inputs[-1] = np.array(training_inputs[-1])
                training_labels[-1] = np.array(training_labels[-1])
                training_inputs.append([])
                training_labels.append([])

            training_inputs[-1].append(_input_)
            training_labels[-1].append(_label_)


        training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 900))
        training_labels[-1] = np.array(training_labels[-1])

        print("    Number of Data points:        ", len(data))
        print("    Number of Training batches:   ", len(training_inputs), "\n")

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

        model = model.to(device)

        running_loss = 0.0
        num_epochs = 5
        for epoch in range(num_epochs):
            for training_input, training_label in zip(training_inputs, training_labels):
                input_tensor = torch.from_numpy(training_input).to(device)
                label_tensor = torch.from_numpy(training_label).long().to(device)

                outputs = model.forward(input_tensor)
                optimizer.zero_grad()
                loss = criterion(outputs, label_tensor)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

        loss = running_loss/(len(training_inputs)*num_epochs)
        print("    Loss: ", loss)

        model = model.cpu()

        correct = 0
        with torch.no_grad():
            input_tensor = torch.from_numpy(test_inputs)
            label_tensor = torch.from_numpy(test_labels).long()

            outputs = model.forward(input_tensor)
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == label_tensor).sum().item()
                
        accuracy = correct/len(test_inputs)
        print("    Accuracy: ", accuracy, "\n")

        if loss < min_loss:
            model.save_weights(f"{model_instance_directory}/predict4_model_min_loss")
            min_loss = loss
        if accuracy > max_accuracy:
            model.save_weights(f"{model_instance_directory}/predict4_model_max_accuracy")
            max_accuracy = accuracy
        
        model.save_weights(f"{model_instance_directory}/predict4_model_most_recent")

        with open(f"{model_instance_directory}/log.csv", "a") as file:
            file.write(f"{iteration},{loss},{accuracy}\n")\

        iteration += 1
