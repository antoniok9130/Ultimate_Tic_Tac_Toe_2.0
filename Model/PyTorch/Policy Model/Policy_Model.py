
import platform
import sys
if platform.platform() == "Windows":
    sys.path.append("..\\..\\..\\")
else:
    sys.path.append("../../../")


import torch
import torch.nn.functional as F
import numpy as np
import random

from UTTT import *

'''
Policy Idea:

Simple Artificial Neural Network with the following feature inputs:

     Feature:                                            | Num Features:
    =====================================================|=======================
     Whether or not they have the quadrants              | 9 * 2           = 18
     Whether or not they have a pair of quadrants        | 9C2 * 2         = 72
     Whether or not they have the square in the quadrant | 81 * 2          = 162
     Whether or not they have a pair within a quadrant   | (9 * 9C2) * 2   = 648
     Whether or not they can take a quadrant             | 9 * 2           = 18
                                                         |
                                                Total:   | 18+72+162+648+18 = 918                 

'''

def extract_features(board): # quadrants, 
    return np.array((board == P1, board == P2))*1.0



class Policy_Model(torch.nn.Module):

    def __init__(self, state_dict_path=None, gamma = 0.95, exploreProb = 0):

        super(Policy_Model, self).__init__()

        self.conv1 = torch.nn.Conv2d(in_channels=2, out_channels=32, kernel_size=3).double()
        # self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3).double()
        self.fc1 = torch.nn.Linear(5*5*64, 256).double()
        self.fc2 = torch.nn.Linear(256, 81).double()
        # self.fc3 = torch.nn.Linear(64, 2).double()
        
        self.softmax = torch.nn.Softmax(dim=-1)

        self.gamma = gamma
        self.exploreProb = exploreProb


        if state_dict_path is not None:
            self.load_state_dict(torch.load(state_dict_path))
            self.eval()

    
    def save_weights(self, state_dict_path: str):
        torch.save(self.state_dict(), state_dict_path)


    def forward(self, x):

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 5*5*64)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return self.softmax(x)

    def predict(self, x):
        return self.forward(torch.tensor(torch.from_numpy(np.reshape(x, (-1, 2, 9, 9))), dtype=torch.double)).detach().numpy()


    def getMove(self, previousMove, quadrants, board):
        legal_moves = getLegalMovesField(quadrants, board, previousMove)
        
        if random.random() < self.exploreProb:
            move = random.choice(legal_moves)

        else:
            action_probabilities = self.predict(extract_features(quadrants, board))
            np.multiply(action_probabilities, legal_moves, action_probabilities)
            move = np.random.choice(np.nonzero(action_probabilities == action_probabilities.max()))

        return int(move//9), move%9


def compute_reward(state: UTTT_Node, policy: Policy_Model):
    winner, time_step = simulation(state, policy.getMove)

    return (1 if winner == state.getPlayer() else -1)*(policy.gamma**time_step)


if __name__ == "__main__":

    policy = Policy_Model()

    # quadrants = np.random.randint(3, size=9)
    # board = np.random.randint(3, size=(9,9))
    # start = current_time_milli()
    # for i in range(1000):
    #     move = policy.getMove(None, quadrants, board)
    # end = current_time_milli()
    # print((end-start)/1000.0)


    # print(compute_reward(UTTT_Node(), policy))

    # policy.save_weights("./ModelInstances/policy2/policy2_model")

    # tensor = torch.tensor(torch.from_numpy(np.random.rand(1002)), dtype=torch.double)
    # tensor = torch.tensor(torch.from_numpy(np.zeros((1002))), dtype=torch.double)

    # model1 = Policy_Model()
    
    # prediction = model1.predict(tensor)

    # print(prediction)
    # print(prediction.argmax())
    # print(np.flatnonzero(prediction == prediction.max()))
    # print(np.random.choice(np.flatnonzero(prediction == prediction.max())))
    # print(len(prediction))
    # print(len(np.unique(prediction)))
    # print(list(model1.parameters())[0][0])

    # model1.save_weights("./ModelInstances/policy1/policy1_model")

    # model2 = UTTT_Model()

    # print(model2.forward(tensor))
    # # print(list(model2.parameters())[0][0])

    # model2.save_weights("./ModelInstances/uttt_conv1_model2")

    # output_tensor = torch.from_numpy(np.array([0.5, 0.5]))
    
    # criterion = torch.nn.BCELoss()
    # optimizer = torch.optim.SGD(model1.parameters(), lr=0.001, momentum=0.9)
    
    # # zero the parameter gradients
    # optimizer.zero_grad()

    # # forward + backward + optimize
    # outputs = model1.forward(tensor)
    # loss = criterion(outputs, output_tensor)
    # loss.backward()
    # optimizer.step()

    # print(loss.item())

