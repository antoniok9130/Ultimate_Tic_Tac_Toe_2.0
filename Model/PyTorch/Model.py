import torch
import numpy as np
import random

# import time
#
# current_time_milli = lambda: int(round(time.time() * 1000))


class UTTT_Model(torch.nn.Module):

    def __init__(self, state_dict_path=None):

        super(UTTT_Model, self).__init__()

        D_in = 180
        # D_h1 = 80 # 120
        # D_h2 = 2 # 80
        D_out = 2
        
        self.linear1 = torch.nn.Linear(D_in, D_out).double()
        self.relu1   = torch.nn.ReLU()
        # self.linear2_1 = torch.nn.Linear(D_h1, D_h2).double()
        # self.linear2_2 = torch.nn.Linear(D_h1, D_h2).double()
        # self.linear2_3 = torch.nn.Linear(D_h1, D_h2).double()
        # self.relu2   = torch.nn.ReLU()
        # self.linear3_1 = torch.nn.Linear(D_h2, D_out).double()
        # self.linear3_2 = torch.nn.Linear(D_h2, D_out).double()
        # self.linear3_3 = torch.nn.Linear(D_h2, D_out).double()
        # self.relu3   = torch.nn.ReLU()
        self.softmax = torch.nn.Softmax(dim=-1)

        if state_dict_path is not None:
            self.load_state_dict(torch.load(state_dict_path))
            self.eval()

        else:
            def init_weights(layer):
                if type(layer) == torch.nn.Linear:
                    torch.nn.init.xavier_normal_(layer.weight)
                    layer.bias.data.fill_(0.01)

            self.apply(init_weights)

    
    def save_weights(self, state_dict_path):
        torch.save(self.state_dict(), state_dict_path)


    def forward(self, input):
        out = self.linear1(input)
        out = self.relu1(out)

        # choice = random.randint(0, 2)
        # if choice == 0:
        #     out = self.linear2_1(out)
        # elif choice == 1:
        #     out = self.linear2_2(out)
        # else:
        #     out = self.linear2_3(out)

        # out = self.relu2(out)

        # choice = random.randint(0, 2)
        # if choice == 0:
        #     out = self.linear3_1(out)
        # elif choice == 1:
        #     out = self.linear3_2(out)
        # else:
        #     out = self.linear3_3(out)

        # out = self.relu3(out)

        return self.softmax(out)


if __name__ == "__main__":

    tensor = torch.tensor([1.]*180, dtype=torch.double)

    model1 = UTTT_Model()

    print(model1.forward(tensor))
    print(model1.forward(tensor).detach().numpy())
    print(list(model1.parameters())[0])

    model1.save_weights("./ModelInstances/uttt_genetic4_model1")

    model2 = UTTT_Model()

    print(model2.forward(tensor))
    print(model2.forward(tensor).detach().numpy())
    print(list(model2.parameters())[0])

    model2.save_weights("./ModelInstances/uttt_genetic4_model2")

    # output_tensor = torch.from_numpy(np.array([0.5, 0.5]))
    
    # criterion = torch.nn.BCELoss()
    # optimizer = torch.optim.SGD(model1.parameters(), lr=0.001, momentum=0.9)
    
    # # zero the parameter gradients
    # optimizer.zero_grad()

    # # forward + backward + optimize
    # outputs = model1.forward(tensor)
    # loss = criterion(outputs, output_tensor)
    # loss.backward()
    # optimizer.step()

    # print(loss.item())

