
import platform
import sys
if platform.platform() == "Windows":
    sys.path.append("..\\..\\..\\")
else:
    sys.path.append("../../../")

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
     Current Length                                      | 1               = 1
     Whether or not they have the quadrants              | 9 * 2           = 18
     Whether or not they have a pair of quadrants        | 9C2 * 2         = 72
     Whether or not they can take a quadrant             | 9 * 2           = 18
     Whether or not they win if they take the quadrant   | 9 * 2           = 18
     Whether or not they have the square in the quadrant | 81 * 2          = 162
     Whether or not they have a pair within a quadrant   | (9 * 9C2) * 2   = 648
                                                         |
                                                Total:   | 18+72+162+648+18 = 918                 

'''

@jit(cache=True)
def extract_features(quadrants, board):

    features = []

    features.extend([
        quadrant == P1 for quadrant in quadrants
    ])
    features.extend([
        quadrant == P2 for quadrant in quadrants
    ])
    features.extend([
        P1 == q1 == q2 for i, q1 in enumerate(quadrants) for j, q2 in enumerate(quadrants) if i < j
    ])
    features.extend([
        P2 == q1 == q2 for i, q1 in enumerate(quadrants) for j, q2 in enumerate(quadrants) if i < j
    ])
    features.extend([
        board[i][j] == P1 for i in range(9) for j in range(9)
    ])
    features.extend([
        board[i][j] == P2 for i in range(9) for j in range(9)
    ])
    features.extend([
        board[i][j] == board[i][k] == P1 for i in range(9) for j in range(9) for k in range(j)
    ])
    features.extend([
        board[i][j] == board[i][k] == P2 for i in range(9) for j in range(9) for k in range(j)
    ])

    return np.array(features)*1.0


input_size = 900

class Predict_Model(torch.nn.Module):

    def __init__(self, state_dict_path=None):

        super(Predict_Model, self).__init__()

        self.fc1__0_15 = torch.nn.Linear(input_size, 256).double()
        self.fc1__15_30 = torch.nn.Linear(input_size, 256).double()
        self.fc1__30_45 = torch.nn.Linear(input_size, 256).double()
        self.fc1__45_60 = torch.nn.Linear(input_size, 256).double()
        self.fc1__60_ = torch.nn.Linear(input_size, 256).double()
        self.fc2 = torch.nn.Linear(256, 3).double()
        
        self.softmax = torch.nn.Softmax(dim=-1)


        if state_dict_path is not None:
            self.load_state_dict(torch.load(state_dict_path))
            self.eval()

    
    def save_weights(self, state_dict_path: str):
        torch.save(self.state_dict(), state_dict_path)


    def forward(self, x, length):
        if length < 15:
            x = F.relu(self.fc1__0_15(x))
        elif 15 <= length < 30:
            x = F.relu(self.fc1__15_30(x))
        elif 30 <= length < 45:
            x = F.relu(self.fc1__30_45(x))
        elif 45 <= length < 60:
            x = F.relu(self.fc1__45_60(x))
        else:
            x = F.relu(self.fc1__60_(x))
        x = F.relu(self.fc2(x))

        return self.softmax(x)

    def predict(self, x, length):

        return self.forward(torch.tensor(torch.from_numpy(x), dtype=torch.double), length).detach().numpy()




if __name__ == "__main__":

    # tensor = torch.tensor(torch.from_numpy(np.random.rand(1002)), dtype=torch.double)
    # tensor = np.random.randint(2, size=900)

    model1 = Predict_Model()

    features = extract_features(np.zeros(9), np.zeros((9, 9)))
    
    prediction = model1.predict(features)

    # print(prediction)
    # print(list(model1.parameters())[0][0])

    # model1.save_weights("../ModelInstances/predict1/predict1_model")

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

