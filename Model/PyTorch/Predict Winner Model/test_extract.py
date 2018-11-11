
import timeit
# import numpy as np
# from Predict_Model import extract_features

# extract_features(np.random.randint(3, size=9), np.random.randint(3, size=(9, 9)))

print(timeit.timeit(
    setup="\n".join([
        "from Predict_Model import extract_features_old", 
        "import numpy as np"]), 
    stmt= "extract_features_old(np.random.randint(3, size=9), np.random.randint(3, size=(9, 9)))", 
    number=10000))
print(timeit.timeit(
    setup="\n".join([
        "from Predict_Model import extract_features", 
        "import numpy as np"]), 
    stmt= "extract_features(np.random.randint(3, size=9), np.random.randint(3, size=(9, 9)))", 
    number=10000))
