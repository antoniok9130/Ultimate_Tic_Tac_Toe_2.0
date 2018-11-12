
import sys
sys.path.append("..\\..\\..\\")

import torch
import torch.nn.functional as F
import numpy as np
from numba import jit
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

# @jit(cache=True)
# def extract_features(quadrants, board):

#     features = []

#     features.extend([
#         quadrant == P1 for quadrant in quadrants
#     ])
#     features.extend([
#         quadrant == P2 for quadrant in quadrants
#     ])
#     features.extend([
#         P1 == q1 == q2 for i, q1 in enumerate(quadrants) for j, q2 in enumerate(quadrants) if i < j
#     ])
#     features.extend([
#         P2 == q1 == q2 for i, q1 in enumerate(quadrants) for j, q2 in enumerate(quadrants) if i < j
#     ])
#     features.extend([
#         board[i][j] == P1 for i in range(9) for j in range(9)
#     ])
#     features.extend([
#         board[i][j] == P2 for i in range(9) for j in range(9)
#     ])
#     features.extend([
#         board[i][j] == board[i][k] == P1 for i in range(9) for j in range(9) for k in range(j)
#     ])
#     features.extend([
#         board[i][j] == board[i][k] == P2 for i in range(9) for j in range(9) for k in range(j)
#     ])

#     return np.array(features)*1.0

@jit
def extract_features(quadrants, board):
    features = np.zeros(900)
    jit_extract_features(features, quadrants, board)
    return features

@jit(nopython=True)
def jit_extract_features(features, quadrants, board):

    n = 0
    for quadrant in quadrants:
        if quadrant == P1:
            features[n] = 1.0
        n += 1
    for quadrant in quadrants:
        if quadrant == P2:
            features[n] = 1.0
        n += 1
    for i, q1 in enumerate(quadrants):
        for j, q2 in enumerate(quadrants):
            if i < j and P1 == q1 == q2:
                features[n] = 1.0
            n += 1
    for i, q1 in enumerate(quadrants):
        for j, q2 in enumerate(quadrants):
            if i < j and P2 == q1 == q2:
                features[n] = 1.0
            n += 1
    for i in range(9):
        for j in range(9):
            if board[i][j] == P1:
                features[n] = 1.0
            n += 1
    for i in range(9):
        for j in range(9):
            if board[i][j] == P2:
                features[n] = 1.0
            n += 1
    for i in range(9):
        for j in range(9):
             for k in range(j):
                if P1 == board[i][j] == board[i][k]:
                    features[n] = 1.0
                n += 1
    for i in range(9):
        for j in range(9):
             for k in range(j):
                if P2 == board[i][j] == board[i][k]:
                    features[n] = 1.0
                n += 1




class Predict_Model(torch.nn.Module):

    def __init__(self, state_dict_path=None):

        super(Predict_Model, self).__init__()

        self.fc1 = torch.nn.Linear(900, 256).double()
        self.fc2 = torch.nn.Linear(256, 3).double()
        # self.fc3 = torch.nn.Linear(64, 2).double()
        
        self.softmax = torch.nn.Softmax(dim=-1)


        if state_dict_path is not None:
            self.load_state_dict(torch.load(state_dict_path))
            self.eval()

    
    def save_weights(self, state_dict_path: str):
        torch.save(self.state_dict(), state_dict_path)


    def forward(self, x):

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return self.softmax(x)

    def predict(self, x):

        return self.forward(torch.tensor(torch.from_numpy(x), dtype=torch.double)).detach().numpy()




if __name__ == "__main__":

    # tensor = torch.tensor(torch.from_numpy(np.random.rand(1002)), dtype=torch.double)
    tensor = np.random.randint(2, size=900)

    model1 = Predict_Model()
    
    prediction = model1.predict(tensor)

    print(prediction)
    print(list(model1.parameters())[0][0])

    model1.save_weights("../ModelInstances/predict1/predict1_model")

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

