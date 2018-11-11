
import timeit
from UTTT import *


print(timeit.timeit(
    # setup="\n".join([
    #     "from numpy import sum",
    #     ]), 
    stmt= "sum([1 for j in range(9) if j == 9])", 
    number=100000))
print(timeit.timeit(
    setup="\n".join([
        "from numpy import sum as np_sum, array as np_array",
        ]), 
    stmt= "np_sum(np_array(1 for j in range(9) if j == 9))", 
    number=100000))



# print(timeit.timeit(
#     setup="\n".join([
#         "import numpy as np",
#         "from UTTT import new_getRandomRemaining"
#         ]), 
#     stmt= "new_getRandomRemaining(np.array([1, 1, 1, 0, 1, 1, 0, 1, 1]))", 
#     number=1000000))
# print(timeit.timeit(
#     setup="\n".join([
#         "import numpy as np",
#         "from UTTT import getRandomRemaining"
#         ]), 
#     stmt= "getRandomRemaining(np.array([1, 1, 1, 0, 1, 1, 0, 1, 1]))", 
#     number=1000000))

# print(timeit.timeit(
#     setup="\n".join([
#         "import numpy as np",
#         "from UTTT import old_check3InRowAt, pairs"
#         ]), 
#     stmt= "old_check3InRowAt(np.zeros(9), 4)", 
#     number=100000))
# print(timeit.timeit(
#     setup="\n".join([
#         "import numpy as np",
#         "from UTTT import check3InRowAt"
#         ]), 
#     stmt= "check3InRowAt(np.zeros(9), 4)", 
#     number=100000))


