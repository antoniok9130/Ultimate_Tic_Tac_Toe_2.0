from time import time

import tensorflow as tf

from Game.GameTree import GameNode


def traverse_tree(node):
    node.increment_visit_count()
    if node.is_leaf():
        return node
    maximum = None
    for child in node.children:
        if maximum is None or child.score > maximum.score:
            maximum = child
    return traverse_tree(maximum)

if __name__ == "__main__":
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())

        start = time()
        root = GameNode()
        current = root
        last_node = None
        i = 0
        while True:
            max = traverse_tree(current)
            if max.game.winner != 0:
                last_node = max
                break
            i += 1
            if i%10 == 0:
                print("i:   ",i,"    ",max.game.gameLength)
            if max.game.gameLength-current.game.gameLength > 10:
                print("Making move      ",current.game.gameLength)
                max_child = None
                for child in current.children:
                    if max_child is None or child.score > max_child.score:
                        max_child = child
                current = max_child
            max.expand_leaf()
            for child in max.children:
                max.update_Q(child.action_value_Q)
        last_node.game.print()
        print(last_node.game.moves)
        end = time()
        print("Took", (end - start), "Seconds to process")