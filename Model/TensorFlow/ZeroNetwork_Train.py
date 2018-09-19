from time import time

import tensorflow as tf
from numpy import array as np_array

from Game.UTTT import UTTT
from Model.TensorFlow.ZeroNetwork import ZeroNetwork


def instantiateModel(version="0.2"):
    with tf.Session() as session:
        zn = ZeroNetwork()
        session.run(tf.global_variables_initializer())

        session.run(tf.global_variables_initializer())

        saver = tf.train.Saver()

        saver.save(session, "./UltimateTicTacToeZero v"+version)

def trainModel(epochs = 200, version="0.2"):
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())

        saver = tf.train.import_meta_graph("./UltimateTicTacToeZero v"+version+'.meta')
        saver.restore(session, tf.train.latest_checkpoint('./'))

        graph = tf.get_default_graph()

        input = graph.get_tensor_by_name("input:0")
        output = graph.get_tensor_by_name("output:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        train_model = graph.get_operation_by_name("train_model")

        print("Training Model")
        update_frequency = epochs/10
        start = time()
        for i in range(epochs):
            if i%100 == 0:
                print("Epoch:   ",i)
            batch = create_UTTT_batch(100)
            session.run(train_model, feed_dict={input:batch[0], output:batch[1], keep_prob:0.5})
        end = time()
        elapsed_time = end - start
        print("Took",elapsed_time,"Seconds to train",epochs,"batches")
        saver.save(session, "./UltimateTicTacToeZero v"+version)

def create_UTTT_batch(batchSize):
    batch = [[], []]
    for i in range(batchSize):
        game = UTTT()
        game.runSimulation()
        batch[0].append(np_array(game.board.board))
        if game.winner == 2:
            batch[1].append(np_array([1, 0, 0]))
        elif game.winner == 1:
            batch[1].append(np_array([0, 1, 0]))
        else:
            batch[1].append(np_array([0, 0, 1]))
    return batch

def testModel(version="0.2"):
    with tf.Session() as session:
        zn = ZeroNetwork()
        session.run(tf.global_variables_initializer())

        saver = tf.train.import_meta_graph("./UltimateTicTacToeZero v"+version+'.meta')
        saver.restore(session, tf.train.latest_checkpoint('./'))

        graph = tf.get_default_graph()

        input = graph.get_tensor_by_name("input:0")
        output = graph.get_tensor_by_name("output:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        accuracy = graph.get_tensor_by_name("accuracy:0")

        batch = create_UTTT_batch(1000)
        a = accuracy.eval(feed_dict={input:batch[0], output:batch[1], keep_prob:1.0})
        print("\nAccuracy:  ",(a*100),"%")

if __name__ == "__main__":
    # instantiateModel()
    # for _ in range(4):
    #     trainModel(1000)
    testModel()

