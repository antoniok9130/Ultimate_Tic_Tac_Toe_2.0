
import sys
sys.path.append("..\..\Game\Python")

import numpy as np
import torch

from UTTT_Logic import *
from random import shuffle
from Model import *

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

            if player == 2:
                game_data.append((np.copy(board), (g, l)))

            board[g][l] = player

            i += 2

        winner = check3InRow([check3InRow(quadrant) for quadrant in board])
    
        for state, move in game_data:

            expected = np.zeros((9, 9))
            expected[move[0]][move[1]] = 1

            data.append((state, expected))
            data.append((np.rot90(state), np.rot90(expected)))
            data.append((np.rot90(state, k=2), np.rot90(expected, k=2)))
            data.append((np.rot90(state, k=3), np.rot90(expected, k=3)))
            data.append((np.fliplr(state), np.fliplr(expected))
            data.append((np.rot90(np.fliplr(state)), np.rot90(np.fliplr(expected))))
            data.append((np.rot90(np.fliplr(state), k=2), np.rot90(np.fliplr(expected), k=2)))
            data.append((np.rot90(np.fliplr(state), k=3), np.rot90(np.fliplr(expected), k=3)))


shuffle(data)

batch_size = 32
training_inputs = [[]]
training_labels = [[]]
test_inputs = []
test_labels = []

for _input_, _label_ in data:
    if len(test_inputs) < len(data)*0.15:
        test_inputs.append(_input_)
        test_labels.append(_label_)
    
    else:
        training_inputs[-1].append(_input_)
        training_labels[-1].append(_label_)

        if len(training_inputs[-1]) >= batch_size:
            training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 1, 9, 9))
            training_labels[-1] = np.array(training_labels[-1])
            training_inputs.append([])
            training_labels.append([])


test_inputs = np.reshape(test_inputs, (-1, 1, 9, 9))
# test_inputs = np.array(test_inputs)
test_labels = np.array(test_labels)

print("Number of Data points:        ", len(data))
print("Number of Training batches:   ", len(training_inputs))
print("Number of Test Points:        ", len(test_inputs))
print()


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Training on:  ", device)

model = UTTT_Model("./ModelInstances/uttt_conv1_model").to(device)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

epochs = 30
iteration_length = 400
iteration = 0
running_loss = 0.0
for epoch in range(epochs):
    print("Epoch:  ", epoch+1)
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
        if iteration >= iteration_length:
            print("    Loss:  ", running_loss/iteration_length)
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
