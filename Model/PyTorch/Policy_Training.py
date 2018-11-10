
import sys
sys.path.append("..\\..\\")
import subprocess as sp

import numpy as np
import torch

from UTTT.Logic import *
from random import shuffle, randint, choice
from Policy_Model import *


import time

current_time_milli = lambda: int(round(time.time() * 1000))


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Training on:  ", device)

policy_name = "./ModelInstances/policy2/policy2_model"
policy = Policy_Model(state_dict_path=policy_name, exploreProb = 0.05)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(policy.parameters(), lr=0.005, momentum=0.9)


running_loss = 0
num_losses = 0

epoch = 1
for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
    for j in [4, 0, 2, 6, 8, 1, 3, 5, 7]:

        start = current_time_milli()

        node = UTTT_Node()

        node.setChild((i, j))
        node = node.getChild(0)
        node.init()

        while node.winner == N:

            expand(node, simulate=False)

            best_children = []
            best_reward = -10
            for i, child in enumerate(node.children):
                child.init()
                reward = compute_reward(child, policy)

                if reward > best_reward:
                    best_children = [i]
                    best_reward = reward

                elif reward == best_reward:
                    best_children.append(i)

            inputs = []
            labels = []
            for i in best_children:
                inputs.append(extract_features(node.getChild(i).buildQuadrant(), node.getChild(i).buildBoard2D()))

                move = node.getChild(i).move
                labels.append(np.array([9*move[0]+move[1]]))

            optimizer.zero_grad()

            inputs = torch.from_numpy(np.reshape(np.array(inputs), (-1, 900)))
            labels = torch.from_numpy(np.reshape(np.array(labels), (-1, ))).long()

            outputs = policy.forward(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            num_losses += 1   

            node.setChild(node.getChild(choice(best_children)).move)
            node = node.getChild(0)
            

        end = current_time_milli()

        print("Time:  ", ((end-start)/1000.0))
        print("Loss:  ", (running_loss/num_losses))

        running_loss = 0
        num_losses = 0

        policy.save_weights(policy_name+"_epoch_"+epoch)
        epoch += 1
