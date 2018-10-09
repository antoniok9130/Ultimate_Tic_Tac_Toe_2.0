
import sys
sys.path.append("..\..\Game\Python")

import numpy as np
import torch

from UTTT_Logic import check3InRowAt, check3InRow
from random import shuffle
from Model import *

P1 = 1
P2 = -1
N = 0
T = 0

# def board_to_input(board):
#     array = np.zeros(180, dtype=np.double)

#     for i in range(9):
#         for j in range(9):
#             spot = board[i][j]

#             if spot == P1:
#                 array[9*i+j] = 1.
#             elif spot == P2:
#                 array[90+9*i+j] = 1.

#         quadrant = check3InRow(board[i])

#         if quadrant == P1:
#             array[81+i] = 1.
#         elif quadrant == P2:
#             array[171+i] = 1.

#     return array


data = []

with open("./Data/RecordedGames.txt") as recordedGames:

    for recordedGame in recordedGames:
        game_data = []
        game = list(recordedGame.strip())

        board = np.zeros((9, 9))

        i = 0
        player = N
        while i < len(game):

            player = P2 if player == P1 else P1

            g = int(game[i])
            l = int(game[i+1])

            board[g][l] = player

            game_data.append((np.copy(board), i))

            i += 2

        winner = check3InRow([check3InRow(quadrant) for quadrant in board])
    
        factor = len(game) * (2 if winner == T else 1)
        for state, length in game_data:
            # reward = 0.5+0.5*(length+1)/factor
            # penalty = 1-reward

            if winner == P1:
                expected = [1.0, 0.0] # [reward, penalty]
            elif winner == P2:
                expected = [0.0, 1.0] # [penalty, reward]
            else:
                expected = [0.5, 0.5]

            data.append((state, expected))
            data.append((np.rot90(state), expected))
            data.append((np.rot90(np.rot90(state)), expected))
            data.append((np.rot90(np.rot90(np.rot90(state))), expected))
            data.append((np.fliplr(state), expected))
            data.append((np.rot90(np.fliplr(state)), expected))
            data.append((np.rot90(np.rot90(np.fliplr(state))), expected))
            data.append((np.rot90(np.rot90(np.rot90(np.fliplr(state)))), expected))

    shuffle(data)

    batch_size = 32
    training_inputs = [[]]
    training_labels = [[]]
    test_inputs = []
    test_labels = []

    for _input_, _label_ in data:
        if len(test_inputs) < len(data)*0.2:
            test_inputs.append(_input_)
            test_labels.append(0 if _label_[0] > _label_[1] else 1)
        
        else:
            if len(training_inputs[-1]) >= batch_size:
                training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 1, 9, 9))
                training_labels[-1] = np.array(training_labels[-1])
                training_inputs.append([])
                training_labels.append([])

            training_inputs[-1].append(_input_)
            training_labels[-1].append(_label_)

    training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 1, 9, 9))
    training_labels[-1] = np.array(training_labels[-1])

    test_inputs = np.reshape(test_inputs, (-1, 1, 9, 9))
    test_labels = np.array(test_labels)

    print("Number of Data points:        ", len(data))
    print("Number of Training batches:   ", len(training_inputs))
    print("Number of Test Points:        ", len(test_inputs))
    print()


    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = UTTT_Model("./ModelInstances/uttt_conv1_model").to(device)

    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    epochs = 2
    iteration = 0
    running_loss = 0.0
    for epoch in range(epochs):
        for _input_, _label_ in zip(training_inputs, training_labels):
            input_tensor = torch.from_numpy(_input_).to(device)
            label_tensor = torch.from_numpy(_label_).to(device)

            optimizer.zero_grad()

            outputs = model.forward(input_tensor)
            loss = criterion(outputs, label_tensor)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            iteration += 1
            if iteration >= 150:
                print("Loss:  ", running_loss/150)
                running_loss = 0.0
                iteration = 0

    model = model.cpu()

    model.save_weights("./ModelInstances/uttt_conv1_model")

    correct = 0
    with torch.no_grad():
        input_tensor = torch.from_numpy(test_inputs)
        label_tensor = torch.from_numpy(test_labels).long()

        outputs = model.forward(input_tensor)
        print(input_tensor.shape)
        print(outputs.shape)
        print(label_tensor.shape)
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == label_tensor).sum().item()

    print("Accuracy:   ", correct/len(test_inputs))
