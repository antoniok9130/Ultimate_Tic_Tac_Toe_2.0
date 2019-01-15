
import time
import sys
import subprocess as sp
from numba import jit
import numpy as np

current_time_milli = lambda: int(round(time.time() * 1000))

def milliseconds_to_time(ms, precision=1):
    num_hours = int(ms//3600000)
    ms -= 3600000*num_hours
    num_minutes = int(ms//60000)
    ms -= 60000*num_minutes
    num_seconds = ms/1000

    time_array = []
    if num_hours > 1:
        time_array.append(f"{num_hours} hrs")
    elif num_hours > 0:
        time_array.append(f"{num_hours} hr")
    if num_minutes > 1:
        time_array.append(f"{num_minutes} mins")
    elif num_minutes > 0:
        time_array.append(f"{num_minutes} min")
    if num_seconds > 0:
        time_array.append(f"{round(num_seconds, precision)} secs")

    return " ".join(time_array)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ProgressBar():

    def __init__(self, end, width=100, clear=False):
        self.end = end
        self.width = width
        self.clear = clear

    def __enter__(self):
        return iter(self)

    def __next__(self):
        self.current += 1
        if self.current >= self.goal:
            self.goal += self.single
            if self.percent < 100:
                self.percent += 1

            print("[{}] {}% | {}".format(("#"*int(self.percent*self.width/100)).ljust(self.width), 
                                        self.percent, 
                                        milliseconds_to_time(current_time_milli()-self.start)
                                        ), end="\r")

    def __exit__(self, type, value, traceback):
        final = "[{}] 100% | {}".format("#"*self.width, milliseconds_to_time(current_time_milli()-self.start, 3))
        if self.clear:
            print(" "*len(final), end="\r")
        else:
            print(final)

    def __iter__(self):
        self.start = current_time_milli()
        self.single = int(self.end//100)
        self.current = 0
        self.goal = 0
        self.percent = -1
        next(self)
        return self



def file_len(file):
    p = sp.Popen(f"wc -l < {file}", stdout=sp.PIPE, shell=True)	
    out, err = p.communicate()
    return int(out)


def argmax(x):
    return np.random.choice(np.flatnonzero(x == x.max()))

def flatten_move(move):
    return 9*move[0]+move[1]

def unflatten_move(move):
    return [int(move//9), int(move%9)]

def cartesian_move(move):
    return [int(3*(move[0]//3)+move[1]//3), int(3*(move[0]%3)+move[1]%3)]


@jit(cache=True, nopython=True)
def product(args, start=1):
    p = start
    for arg in args:
        p *= arg
    return p



@jit(cache=True, nopython=True)
def rot90(g, l, k=1, flip=False, cartesian=True):

    # convert to cartesian coordinates with origin at center, center
    if cartesian:
        x = int(3*(g%3)+l%3)-4
        y = 4-int(3*(g//3)+l//3)
    else:
        x = 4-g
        y = l-4

    if flip: x = -x

    # rotate coordinates
    for i in range(k):
        x, y = y, -x

    # convert back to global, local
    x = x+4
    y = 4-y
    g = 3*(y//3)+(x//3)
    l = 3*(y%3)+(x%3)

    return [g, l]

# @jit(cache=True)
def board_rot90(board, k=1, flip=False):
    if flip:
        if k == 0:
            return [np.fliplr(b) for b in board]
        elif k == 2:
            return [np.fliplr(b) for b in np.rot90(board, k=k, axes=(1, 2))]
        else:
            return np.rot90(np.fliplr(board), k=k, axes=(1, 2))
    else:
        return np.rot90(board, k=-k, axes=(1, 2))


# @jit(cache=True, nopython=True)
# def softmax(x):
#     e_x = np.exp(x - np.max(x))
#     return e_x / e_x.sum(axis=0)



if __name__ == "__main__":
    assert(rot90(0, 0) == [2, 2])
    assert(rot90(2, 3) == [8, 1])
    assert(rot90(4, 4) == [4, 4])
    assert(rot90(3, 2) == [1, 8])
    assert(rot90(3, 2, 2) == [5, 6])
    assert(rot90(3, 2, 3) == [7, 0])
    assert(rot90(3, 2, 3, True) == [1, 6])

    for i in range(81):
        board1 = np.zeros((2, 9, 9))
        board2 = np.zeros((2, 9, 9))

        action = unflatten_move(i)
        xy = cartesian_move(action)
        board1[0][xy[0]][xy[1]] = 1

        for flip in [True, False]:
            for k in range(4):
                board2 = np.zeros((2, 9, 9))

                transformed_action = rot90(action[0], action[1], k=k, flip=flip)
                xy = cartesian_move(transformed_action)
                board2[0][xy[0]][xy[1]] = 1

                if flip:
                    if k == 0:
                        transformed_board = np.array([np.fliplr(b) for b in board1])
                    elif k == 2:
                        transformed_board = np.array([np.fliplr(b) for b in np.rot90(board1, k=k, axes=(1, 2))])
                    else:
                        transformed_board = np.rot90(np.fliplr(board1), k=k, axes=(1, 2))
                else:
                    transformed_board = np.rot90(board1, k=-k, axes=(1, 2))

                if not all(list((transformed_board == board2).ravel())):
                    print("Flip: ", flip)
                    print("K:    ", k, "\n")
                    print(action)
                    print(board1[0])
                    print(transformed_board[0])
                    print(board2[0],"\n")

    # print("Action:  ", action)
    # print("XY:      ", xy)
    # print(board1, "\n")


    # flip = True if np.random.randint(2) == 1 else False
    # k = np.random.randint(4)
    # print("Flip: ", flip)
    # print("K:    ", k, "\n")

    # transformed_action = rot90(action[0], action[1], k=k, flip=flip)
    # xy = cartesian_move(transformed_action)
    # board2[0][xy[0]][xy[1]] = 1
    
    # print("Action:  ", transformed_action)
    # print("XY:      ", xy)

    # if flip:
    #     board1 = np.fliplr(np.rot90(board1, k=-k, axes=(1, 2)))
    # else:
    #     board1 = np.rot90(board1, k=-k, axes=(1, 2))
    
    # print(board1, "\n")
    # print(board2, "\n")
    # print(all(list((board1 == board2).ravel())))




