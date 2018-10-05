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
        self.linear2 = torch.nn.Linear(120, 81).double()
        self.relu2   = torch.nn.ReLU()
        self.linear3 = [
            torch.nn.Linear(81, 2).double(),
            torch.nn.Linear(81, 2).double(),
            torch.nn.Linear(81, 2).double()
        ]
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, input):
        out = self.linear1(input)
        out = self.relu1(out)
        out = self.linear2(out)
        out = self.relu2(out)
        out = self.linear3[random.randint(0, 2)](out)
        return self.softmax(out)


if __name__ == "__main__":

    model = UTTT_Model()


    # model = torch.load("./ModelInstances/test1_trained").double()
    #
    # parameters1 = list(model1.parameters())
    # detached1 = [parameters1[i].detach().numpy() for i in range(len(parameters1))]
    #
    # model2 = torch.load("./ModelInstances/test1_trained2")
    #
    # parameters2 = list(model2.parameters())
    # detached2 = [parameters2[i].detach().numpy() for i in range(len(parameters2))]
    #
    # # for d in detached:
    # #     print(d.shape)
    #
    # print(detached1[0][0][:6])
    # print(detached2[0][0][:6])


    # start = current_time_milli()
    #
    tensor = torch.tensor([1.]*180, dtype=torch.double)
    print(model.forward(tensor))
    print(model.forward(tensor).detach().numpy())
    #
    # for i in range(1600):
    #     value = model.forward(tensor)
    #
    # print(current_time_milli() - start)

    torch.save(model.state_dict(), "./ModelInstances/uttt_model1")
