
import os
import sys
sys.path.append("../../../")

from numba import jit
import numpy as np
from random import shuffle

from UTTT import *
from Predict_Model import *

model = Predict_Model()

@jit
def modelSimulation(quadrants, board, winner, move, player):
    '''
    Parameters
    ----------
    quadrants : 1d list
        a list of length nine representing the current quadrant state
    board : 2d list
        a 2d list of length nine by nine representing the current board state
    winner : int
        the winner if any
    move : 1d list
        a list of length two containing the quadrant and square of the previous move
    player : int
        the current player

    Returns
    ----------
    winner : int
        an int signifying the predicted winner
    length : int
        how far into the future the win occured
    '''
    
    if winner != N:
        return winner, 0
    
    if move is not None and quadrants[move[1]] == N:
        if potential3inRow_wp(quadrants, move[1], player):
            return player, 1 # next move
    else:
        for g in range(9):
            if quadrants[g] == N and potential3inRow_wp(quadrants, g, player):
                return player, 1 # next move

    prediction = model.predict(extract_features(quadrants, board))
    winner = prediction.argmax()
    # print(prediction)
    if winner == 0:
        return T, 2 # at least two into the future
    if winner == 1:
        return P1, 2 # at least two into the future
    if winner == 2:
        return P2, 2 # at least two into the future



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Training on:  ", device)

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

            
with open("../ModelInstances/predict3/log.csv", "w") as file:
    file.write("iteration,duration,loss,accuracy,start,game,winner\n")

numP1Wins = 0
numP2Wins = 0
numTies = 0

min_loss = 1000
max_accuracy = -1000

iteration = 1
while True:
    for g in range(9):
        for l in range(9):

            print("Iteration:", iteration)
            try:
                node = MCTS_Node()
                node.setChild([g, l])
                node = node.getChild(0)

                game_data = []
                moves = []

                start = current_time_milli()

                while node.winner == N:
                    move = getMove(node, iterations=1600, simulation=modelSimulation)
                    moves.append(move)
                    node.setChild(move)
                    node = node.getChild(0)
                    game_data.append((node.buildBoard2D(), np.reshape(node.buildQuadrant(), (3, 3))))
                    # print(f"g:   {move[0]}      l:   {move[1]}")
                    # print(f"w:   {node.numWins}      v:   {node.numVisits}")
                    # print(f"confidence:   {node.getConfidence()}")
                    # print(f"time:         {(end-start)/1000.0} seconds")
                
                end = current_time_milli()

                duration = (end-start)/1000.0
                print("    Time: ", duration)

                data = []

                if node.winner == P1:
                    expected = 1 # [reward, penalty]
                    numP1Wins += 1
                elif node.winner == P2:
                    expected = 2 # [penalty, reward]
                    numP2Wins += 1
                else:
                    expected = 0
                    numTies += 1

                for board, quadrants in game_data:
                    # reward = 0.5+0.5*(length+1)/factor
                    # penalty = 1-reward

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
                    model.save_weights(f"../ModelInstances/predict3/predict3_model_min_loss")
                    min_loss = loss
                if accuracy > max_accuracy:
                    model.save_weights(f"../ModelInstances/predict3/predict3_model_max_accuracy")
                    max_accuracy = accuracy
             
                model.save_weights(f"../ModelInstances/predict3/predict3_model_most_recent")

                with open("../ModelInstances/predict3/log.csv", "a") as file:
                    file.write(f"{iteration},{duration},{loss},{accuracy},[{g} {l}],{''.join(f'{move[0]}{move[1]}' for move in moves)},{node.winner}\n")


            except:
                print("An Exception was thrown")


            modelSimulation.recompile()

            iteration += 1
            






