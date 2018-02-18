from time import time

import tensorflow as tf
from numpy import array as np_array

import Model.ZeroNetwork as zn
from Game.UTTT import UTTT


def make_move(game):
    moves = []
    if game.gameLength == 0:
        moves = [[i, j] for i in range(9) for j in range(9)]
    elif game.grid3by3[game.moves[-1][1]] == 0:
        i = game.moves[-1][1]
        moves = [[i, j] for j in game.board2dLeft[i]]
    else:
        moves = [[i, j] for i in game.grid3by3Left
                 for j in game.board2dLeft[i]]

    best_move = None
    for move in moves:
        possible = UTTT(game)
        possible.add_move(move[0], move[1])
        score = zn.valuate(zn.model.eval(
            feed_dict={zn.input: np_array([possible.board.board]), zn.keep_prob: 1}))
        if best_move is None or score > best_move[2]:
            best_move = [move[0], move[1], score]

    game.add_move(best_move[0], best_move[1])

if __name__ == "__main__":

    with tf.Session() as session:
        session.run(tf.global_variables_initializer())

        start = time()
        game = UTTT()
        while game.winner == 0:
            make_move(game)
        end = time()
        print("Took", (end - start), "Seconds to process")
