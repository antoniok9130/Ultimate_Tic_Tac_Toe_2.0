
import sys
sys.path.append("../../Game/Python")

from UTTT_Logic import *
from NN_MCTS_Node import NN_MCTS_Node as Node
from NN_MCTS import NN_MCTS as MCTS, board_to_input
from Model import UTTT_Model
from random import shuffle

import time
import torch
import numpy as np

current_time_milli = lambda: int(round(time.time() * 1000))

iteration = 1
total_generate_time = 0
total_training_time = 0

model = UTTT_Model()
model.load_state_dict(torch.load("./ModelInstances/uttt_model1_trained"))
model.eval()
    
mcts = MCTS(model)

criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

while True:

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
        reward = 0.5+0.5*(length+1)/i
        penalty = 1-reward

        data.append([board_to_input(state), np.array([reward, penalty] if node.getWinner() == P1 else [penalty, reward])])

    shuffle(data)
    # data = np.reshape(data, [-1, 50, 2])

    end = current_time_milli()
    generate_time = (end-start)
    total_generate_time += generate_time
    start = current_time_milli()
    
    
    # get the inputs
    input, label = zip(*data)

    input_tensor = torch.from_numpy(np.array(input))
    output_tensor = torch.from_numpy(np.array(label))
    
    # zero the parameter gradients
    optimizer.zero_grad()

    # forward + backward + optimize
    outputs = model.forward(input_tensor)
    loss = criterion(outputs, output_tensor)
    loss.backward()
    optimizer.step()

    # print statistics
    running_loss = loss.item()

    end = current_time_milli()  


    total_training_time += (end-start)

    torch.save(model.state_dict(), "./ModelInstances/uttt_model1_trained")

    print(f"Iteration {iteration} took {(generate_time+end-start)/1000.0} seconds to complete")
    print("   ", "Winner:         ", node.getWinner())
    print("   ", "Game Length:    ", i)
    print("   ", "Loss:           ", running_loss)
    print("   ", "Generate Time:   {0:.3f}    Avg:  {1:.3f}".format(generate_time, total_generate_time/float(1000*iteration)))
    print("   ", "Training Time:   {0:.3f}    Avg:  {1:.3f}".format((end-start)/1000.0, total_training_time/float(1000*iteration)))

    iteration += 1
