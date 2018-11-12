
import sys
sys.path.append("..\\..\\")

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

@jit(cache=True)
def extract_features(quadrants, board):

    features = []

    features.extend(quadrants)
    for quadrant in board:
        features.extend(board)

    return np.array(features)



class Policy_Model(torch.nn.Module):

    def __init__(self, state_dict_path=None, gamma = 0.95, exploreProb = 0):

        super(Policy_Model, self).__init__()

        self.fc1 = torch.nn.Linear(90, 256).double()
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

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return self.softmax(x)

    def predict(self, x):
        return self.forward(torch.tensor(torch.from_numpy(x), dtype=torch.double)).detach().numpy()


    def getMove(self, previousMove, quadrants, board):
        legal_moves = []
        if previousMove is not None and quadrants[previousMove[1]] == N:
            g = previousMove[1]
            legal_moves = [9*g+l for l in range(9) if board[g][l] == N]
        
        else:
            legal_moves = [9*g+l for g in range(9) if quadrants[g] == N for l in range(9) if board[g][l] == N]

        if len(legal_moves) <= 0:
            raise Exception("No Legal Moves")
        
        if random.random() < self.exploreProb:
            move = random.choice(legal_moves)

        else:
            action_probabilities = self.predict(extract_features(quadrants, board))

            max_prob = -1
            best_moves = []
            for legal_move in legal_moves:
                probability = action_probabilities[legal_move]
                if probability > max_prob:
                    max_prob = probability
                    best_moves = [legal_move]
                elif probability == max_prob:
                    best_moves.append(legal_move)

            move = random.choice(best_moves)

        return int(move//9), move%9


def compute_reward(state: UTTT_Node, policy: Policy_Model):
    winner, time_step = simulation(state, policy.getMove)

    return (1 if winner == state.getPlayer() else -1)*(policy.gamma**time_step)


if __name__ == "__main__":

    policy = Policy_Model()

    print(compute_reward(UTTT_Node(), policy))

    policy.save_weights("./ModelInstances/policy2/policy2_model")

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

