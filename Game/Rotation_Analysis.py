import numpy as np

board = np.zeros((9, 9))

needed = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2),
          (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4),
          (3, 3), (3, 4), (4, 4)]
for g, l in needed:
    board[g][l] = 1

print(board)

# rotated = np.rot90(board)
# flipped = np.fliplr(board)
# for _ in range(3):
#     for i in range(9):
#         for j in range(9):
#             if (int(rotated[i][j]) == 1):
#                 board[i][j] = int(board[i][j]) | int(rotated[i][j])
#
#             if (int(flipped[i][j]) == 1):
#                 board[i][j] = int(board[i][j]) | int(flipped[i][j])
#     rotated = np.rot90(rotated)
#     flipped = np.rot90(flipped)

print(board)
