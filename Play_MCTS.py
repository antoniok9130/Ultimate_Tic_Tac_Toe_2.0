from UTTT import *


# play_UTTT()




for i in range(10):
    board = np.zeros((9, 9))
    move = unflatten_move(np.random.randint(81))
    board[move[0]][move[1]] = 1
    rotated = rot90(move[0], move[1])
    board = unravel_board(board)
    board = np.rot90(board)
    assert(board)

