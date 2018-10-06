import torch
import numpy
import random

# import time
#
# current_time_milli = lambda: int(round(time.time() * 1000))

class UTTT_Model(torch.nn.Module):

    def __init__(self):

        super(UTTT_Model, self).__init__()
        
        self.linear1 = torch.nn.Linear(180, 120).double()
        self.relu1   = torch.nn.ReLU()
        self.linear2 = [
            torch.nn.Linear(120, 81).double(),
            torch.nn.Linear(120, 81).double(),
            torch.nn.Linear(120, 81).double()
        ]
        self.relu2   = torch.nn.ReLU()
        self.linear3 = [
            torch.nn.Linear(81, 2).double(),
            torch.nn.Linear(81, 2).double(),
            torch.nn.Linear(81, 2).double()
        ]
        self.relu3   = torch.nn.ReLU()
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, input):
        out = self.linear1(input)
        out = self.relu1(out)
        out = self.linear2[random.randint(0, 2)](out)
        out = self.relu2(out)
        out = self.linear3[random.randint(0, 2)](out)
        out = self.relu3(out)
        return self.softmax(out)


if __name__ == "__main__":

    tensor = torch.tensor([1.]*180, dtype=torch.double)

    model1 = UTTT_Model()

    print(model1.forward(tensor))
    print(model1.forward(tensor).detach().numpy())
    print(list(model1.parameters())[0])

    torch.save(model1.state_dict(), "./ModelInstances/uttt_genetic_model1")

    model2 = UTTT_Model()

    print(model2.forward(tensor))
    print(model2.forward(tensor).detach().numpy())
    print(list(model2.parameters())[0])

    torch.save(model2.state_dict(), "./ModelInstances/uttt_genetic_model2")
