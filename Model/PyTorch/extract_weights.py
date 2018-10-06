
from Model import *
import numpy as np

model = UTTT_Model()
model.load_state_dict(torch.load("./ModelInstances/uttt_genetic2_model1"))
model.eval()

params = np.array(list(model.parameters()))

print("Param shapes:")
for param in params:
    print("   ", param.shape)