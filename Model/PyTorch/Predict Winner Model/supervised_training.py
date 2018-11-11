
import sys
sys.path.append("..\\..\\..\\")
import subprocess as sp

import numpy as np
import torch
from math import ceil

from UTTT import *
from random import shuffle
from Predict_Model import *

data = []

file_name = "../Data/RecordedGames.txt"
p = sp.Popen("wc -l < "+file_name, stdout=sp.PIPE, shell=True)
out, err = p.communicate()

num_records = int(out)
percentile = 1
space = ceil(100/percentile)
division = ceil(num_records/space)


with open(file_name) as recordedGames:

    percent = 0
    progress = 0
    milestone = division
    print("Loading Data")
    for recordedGame in recordedGames:
        progress += 1
        if (progress >= milestone):
            percent += 1
            milestone += division
            print("[{}] {}%".format(("#"*percent).ljust(space), percent*percentile), end="\r")
            # sys.stdout.flush()

        
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

            game_data.append((np.copy(board), np.copy(quadrants)))

            i += 2

        winner = check3InRow([quadrants[g][l] for g in range(3) for l in range(3)])
    
        factor = len(game) * (2 if winner == T else 1)
        for board, quadrants in game_data:
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

    percent += 1
    print("[{}] {}%".format(("#"*percent).ljust(space), percent*percentile))
            


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
        if len(training_inputs[-1]) >= batch_size:
            training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 900))
            # training_inputs[-1] = np.array(training_inputs[-1])
            training_labels[-1] = np.array(training_labels[-1])
            training_inputs.append([])
            training_labels.append([])

        training_inputs[-1].append(_input_)
        training_labels[-1].append(_label_)

training_inputs[-1] = np.reshape(training_inputs[-1], (-1, 900))
# training_inputs[-1] = np.array(training_inputs[-1])
training_labels[-1] = np.array(training_labels[-1])

test_inputs = np.reshape(test_inputs, (-1, 900))
# test_inputs = np.array(test_inputs)
test_labels = np.array(test_labels)

print("Number of Data points:        ", len(data))
print("Number of Training batches:   ", len(training_inputs))
print("Number of Test Points:        ", len(test_inputs), "\n")


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Training on:  ", device)

model = Predict_Model("../ModelInstances/predict1/predict1_model")

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

iteration_length = 400
iteration = 0
running_loss = 0.0
with open("../ModelInstances/predict1/training_data.csv", "a") as file:
    file.write("epoch,loss,accuracy\n")
    for epoch in range(250):
        model = model.to(device)
        print("Epoch: ", epoch)
        for _input_, _label_ in zip(training_inputs, training_labels):
            input_tensor = torch.from_numpy(_input_).to(device)
            label_tensor = torch.from_numpy(_label_).long().to(device)

            optimizer.zero_grad()

            outputs = model.forward(input_tensor)
            loss = criterion(outputs, label_tensor)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            iteration += 1

        
        model = model.cpu()

        correct = 0
        with torch.no_grad():
            input_tensor = torch.from_numpy(test_inputs)
            label_tensor = torch.from_numpy(test_labels).long()

            outputs = model.forward(input_tensor)
            # print(input_tensor.shape)
            # print(outputs.shape)
            # print(label_tensor.shape)
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == label_tensor).sum().item()

        print("    Loss:     ", running_loss/iteration)
        print("    Accuracy: ", correct/len(test_inputs))
        file.write(f"{epoch},{running_loss/iteration},{correct/len(test_inputs)}\n")

        running_loss = 0.0
        iteration = 0

        model.save_weights(f"../ModelInstances/predict1/predict1_model_epoch_{epoch}")
