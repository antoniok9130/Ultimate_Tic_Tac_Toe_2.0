import torch

# import time
#
# current_time_milli = lambda: int(round(time.time() * 1000))

model = torch.nn.Sequential(
    torch.nn.Linear(180, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100, 81),
    torch.nn.ReLU(),
    torch.nn.Linear(81, 9),
    torch.nn.ReLU(),
    torch.nn.Linear(9, 2)
)

# model = torch.load("./ModelInstances/test2")

# start = current_time_milli()
#
# tensor = torch.tensor([1.]*180)
#
# for i in range(1600):
#     value = model.forward(tensor)
#
# print(current_time_milli() - start)

torch.save(model, "./ModelInstances/test1")