
import sys
sys.path.append("../../")

import torch

from UTTT.Logic import *
from UTTT.utils import *
from Model import *


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Validating on:  ", device)

model = UTTT_Model("./Attempts/supervised6/most_recent_uttt_model").to(device)

def getMoves(record):
    return [[int(record[i]), int(record[i+1])] for i in range(0, len(record), 2)]

def validate():
    with open("./Data/ValidationGames.txt") as file:
        games = [getMoves(row.strip()) for row in file]

    start = 1

    numCorrectPolicies = 0
    totalPoliciesChecked = 0
    valuesLoss = 0
    totalValuesChecked = 0
    # boards = []
    for e, game in enumerate(games):
        boards = []
        policy_labels = []
        board = np.zeros((9, 9))
        for i, move in enumerate(game):
            if i >= start:
                boards.append(np.copy(transform_board(unravel_board(board))))
                policy_labels.append(flatten_move(move))

            board[move[0]][move[1]] = i%2+1

        winner = check3InRow([check3InRow(board[g]) for g in range(9)])
        if winner == P1:
            value_labels = [(-1)**i for i in range(start, len(boards)+start)]
        elif winner == P2:
            value_labels = [(-1)**(i+1) for i in range(start, len(boards)+start)]
        else:
            value_labels = [0 for i in range(start, len(boards)+start)]

        policies, values = model.predict(np.array(boards, dtype=np.double), device)
        for p, l in zip(policies, policy_labels):
            if argmax(p) == l:
                numCorrectPolicies += 1
            totalPoliciesChecked += 1

        for v, l in zip(values, value_labels):
            valuesLoss += abs(v-l)
            totalValuesChecked += 1

        if e%10 == 0:
            print("\rGame:", str(e).ljust(7), 
                    "Policy Accuracy: ", str(round(numCorrectPolicies/totalPoliciesChecked, 6)).ljust(10), 
                    "Average Loss: ", str(round(valuesLoss/totalValuesChecked, 6)).ljust(10), end="")
                    
    print()




if __name__ == "__main__":
    validate()
