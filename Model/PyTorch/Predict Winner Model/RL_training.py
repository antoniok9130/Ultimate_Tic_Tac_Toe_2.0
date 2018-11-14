
import sys
sys.path.append("../../../")

from numba import jit
import numpy as np
from random import shuffle

from UTTT import *
from Predict_Model import *

model = Predict_Model("../ModelInstances/predict2_model_iter_278")

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

numP1Wins = 0
numP2Wins = 0
numTies = 0

iteration = 279
while True:
    print("Iteration:", iteration)
    sys.stdout.flush()
    try:
        node = MCTS_Node()
        game_data = []

        start = current_time_milli()

        while node.winner == N:
            move = getMove(node, iterations=1600, simulation=modelSimulation)
            node.setChild(move)
            node = node.getChild(0)
            game_data.append((node.buildBoard2D(), np.reshape(node.buildQuadrant(), (3, 3))))
            # print(f"g:   {move[0]}      l:   {move[1]}")
            # print(f"w:   {node.numWins}      v:   {node.numVisits}")
            # print(f"confidence:   {node.getConfidence()}")
            # print(f"time:         {(end-start)/1000.0} seconds")
        
        end = current_time_milli()

        print("    Time: ", (end-start)/1000.0)
        sys.stdout.flush()

        data = []

        for board, quadrants in game_data:
            # reward = 0.5+0.5*(length+1)/factor
            # penalty = 1-reward

            if node.winner == P1:
                expected = 1 # [reward, penalty]
                numP1Wins += 1
            elif node.winner == P2:
                expected = 2 # [penalty, reward]
                numP2Wins += 1
            else:
                expected = 0
                numTies += 1

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
        sys.stdout.flush()

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

        model = model.to(device)

        running_loss = 0.0
        for training_input, training_label in zip(training_inputs, training_labels):
            input_tensor = torch.from_numpy(training_input).to(device)
            label_tensor = torch.from_numpy(training_label).long().to(device)

            outputs = model.forward(input_tensor)
            optimizer.zero_grad()
            loss = criterion(outputs, label_tensor)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        correct = 0
        with torch.no_grad():
            for training_input, training_label in zip(training_inputs, training_labels):
                input_tensor = torch.from_numpy(training_input).to(device)
                label_tensor = torch.from_numpy(training_label).long().to(device)

                outputs = model.forward(input_tensor)
                _, predicted = torch.max(outputs.data, 1)
                correct += (predicted == label_tensor).sum().item()
                

        print("    Accuracy: ", correct/len(data))
        print("    Loss: ", running_loss/len(training_inputs))
        sys.stdout.flush()

        model = model.cpu()

        model.save_weights(f"../ModelInstances/predict2/predict2_model_iter_{iteration}")

        with open("../ModelInstances/predict2/losses.csv", "a") as file:
            file.write(f"{iteration},{running_loss/len(training_inputs)}")

    except:
        pass


    modelSimulation.recompile()

    iteration += 1





