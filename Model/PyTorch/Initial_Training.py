
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from UTTT_Logic import N, P1, P2, check3InRowAt, check3InRow


def board_to_input(board):
    array = np.zeros(180, dtype=np.double)

    for i in range(9):
        for j in range(9):
            spot = board[i][j]

            if spot == P1:
                array[9*i+j] = 1.
            elif spot == P2:
                array[90+9*i+j] = 1.

        quadrant = check3InRow(board[i])

        if quadrant == P1:
            array[81+i] = 1.
        elif quadrant == P2:
            array[171+i] = 1.

    return array


# array = np.zeros(180)
#
# if player == P1:
#     array[9 * g + l] = 1
# else:
#     array[90 + 9 * g + l] = 1
#
# if quadrants[g] == P1:
#     array[81 + g] = 1
# elif quadrants[g] == P2:
#     array[171 + g] = 1


with open("./Data/RecordedGames.txt") as recordedGames:

    model = torch.load("./ModelInstances/test1_trained")
    model = model.double()

    data = []

    for recordedGame in recordedGames:

        game_data = []

        game = list(recordedGame.strip())

        board = np.zeros((9, 9))
        quadrants = np.zeros(9)

        i = 0
        player = N
        while i < len(game):

            player = P2 if player == P1 else P1

            g = int(game[i])
            l = int(game[i+1])

            board[g][l] = player
            quadrants[g] = check3InRowAt(board[g], l)

            rotated = np.copy(board)
            game_data.append(rotated)
            for _ in range(3):
                rotated = np.rot90(rotated)
                game_data.append(rotated)

            flipped = np.fliplr(board)
            game_data.append(flipped)
            for _ in range(3):
                flipped = np.rot90(flipped)
                game_data.append(flipped)


            i += 2

        winner = check3InRow(quadrants)

        for d in game_data:
            data.append((board_to_input(d), np.array([1., 0.] if winner == P1 else [0., 1.])))

    print(len(data))

    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    running_loss = 0.0
    for i, data in enumerate(data):
        # get the inputs
        input, label = data

        input_tensor = torch.from_numpy(input)
        output_tensor = torch.from_numpy(label)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(input_tensor)
        loss = criterion(outputs, output_tensor)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 1000 == 1999:  # print every 2000 mini-batches
            print('loss:  {0}'.format(running_loss / 2000))
            running_loss = 0.0

    torch.save(model, "./ModelInstances/test1_trained2")
