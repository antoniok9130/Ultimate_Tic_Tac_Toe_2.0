
import sys
sys.path.append("../../Game/Python")

from UTTT_Logic import *
from NN_MCTS_Node import NN_MCTS_Node as Node
from NN_MCTS import NN_MCTS as MCTS, board_to_input
from Model import UTTT_Model
from random import shuffle, randint

import time
import torch
import numpy as np

current_time_milli = lambda: int(round(time.time() * 1000))

iteration = 1
total_generate_time = 0
total_training_time = 0

criterion = torch.nn.BCELoss()

while True:

    model1 = UTTT_Model()
    model1.load_state_dict(torch.load("./ModelInstances/uttt_genetic2_model1"))
    model1.eval()

    model2 = UTTT_Model()
    model2.load_state_dict(torch.load("./ModelInstances/uttt_genetic2_model2"))
    model2.eval()
        
    mcts = MCTS(model1, model2)

    start = current_time_milli()

    game_data = []

    board = np.zeros((9, 9))
    quadrants = np.zeros(9)

    node = Node()

    i = 0
    while node.getWinner() == N:
        g, l = mcts.getMove(node)
        node.setChild([g, l])
        node = node.getChild(0)

        board[g][l] = node.getPlayer()
        quadrants[g] = check3InRowAt(board[g], l)

        rotated = np.copy(board)
        game_data.append((rotated, i))
        flipped = np.fliplr(board)
        game_data.append((flipped, i))
        for _ in range(3):
            rotated = np.rot90(rotated)
            game_data.append((rotated, i))
            flipped = np.rot90(flipped)
            game_data.append((flipped, i))

        i += 1

    
    data = []

    for state, length in game_data:
        reward = 0.5+0.5*(length+1)/(i * (2 if node.getWinner() == T else 1))
        penalty = 1-reward
        expected = [reward, penalty]

        if node.getWinner() == P1:
            data.append([board_to_input(state), np.array(expected)])
        
        elif node.getWinner() == P2:
            data.append([board_to_input(state), np.array(expected[::-1])])

        else:
            shuffle(expected)
            data.append([board_to_input(state), np.array(expected)])


    shuffle(data)
    batches = [[]]
    
    for d in data:
        if len(batches[-1]) >= 32:
            batches.append([])

        batches[-1].append(d)

    end = current_time_milli()
    generate_time = (end-start)
    total_generate_time += generate_time
    start = current_time_milli()
    
    model = UTTT_Model()
    if node.getWinner() != T:
        model.load_state_dict(torch.load("./ModelInstances/uttt_genetic2_model"+str(node.getWinner())))
    else:
        model.load_state_dict(torch.load("./ModelInstances/uttt_genetic2_model"+str(randint(1, 2))))

    model.eval()

    optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    
    running_loss = 0
    for batch in batches:
        # get the inputs
        input_data, label = zip(*batch)

        input_tensor = torch.from_numpy(np.array(input_data))
        output_tensor = torch.from_numpy(np.array(label))
        
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model.forward(input_tensor)
        loss = criterion(outputs, output_tensor)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()

    running_loss /= len(batches)

    save_model2_to_model1 = node.getWinner() == P2 or (node.getWinner() != P1 and randint(1, 2) == 2)

    if save_model2_to_model1:
        torch.save(model2.state_dict(), "./ModelInstances/uttt_genetic2_model1")

    torch.save(model.state_dict(), "./ModelInstances/uttt_genetic2_model2")

    if iteration%25 == 0:
        try:
            timestamp = str(current_time_milli())
            if save_model2_to_model1:
                torch.save(model2.state_dict(), "./ModelInstances/Cache/uttt_genetic2_model1_"+timestamp)
            else:
                torch.save(model1.state_dict(), "./ModelInstances/Cache/uttt_genetic2_model1_"+timestamp)
            
            torch.save(model.state_dict(), "./ModelInstances/Cache/uttt_genetic2_model2_"+timestamp)
        except Exception:
            pass

    end = current_time_milli()  


    total_training_time += (end-start)

    print(f"Iteration {iteration} took {(generate_time+end-start)/1000.0} seconds to complete")
    print("   ", "Winner:         ", node.getWinner())
    print("   ", "Game Length:    ", i)
    print("   ", "Loss:           ", running_loss)
    print("   ", "Generate Time:   {0:.3f}    Avg:  {1:.3f}".format(generate_time/1000.0, total_generate_time/float(1000*iteration)))
    print("   ", "Training Time:   {0:.3f}    Avg:  {1:.3f}".format((end-start)/1000.0, total_training_time/float(1000*iteration)))

    iteration += 1
