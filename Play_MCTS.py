from UTTT import *
import profile

node = MCTS_Node()
node.setChild([4, 4])
node = node.getChild(0)
node.init()

start = current_time_milli()


# profile.run("getMove(node, iterations=1000)")
move = getMove(node, iterations=3200)
node.setChild(move)
node = node.getChild(0)

end = current_time_milli()

print("3200 iterations performed in", (end-start)/1000.0, "seconds")
# print("Confidence:  ", node.getConfidence())

# import timeit

# print(timeit.timeit("np.random.choice(9, 90)", "import numpy as np"))
# print(timeit.timeit("np.random.randint(9, size=90)", "import numpy as np"))