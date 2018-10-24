import torch
import torch.nn.functional as F
import numpy as np
import random

# import time
#
# current_time_milli = lambda: int(round(time.time() * 1000))


class UTTT_Model(torch.nn.Module):

    def __init__(self, state_dict_path=None):

        super(UTTT_Model, self).__init__()

        self.conv1 = torch.nn.Conv2d(in_channels=2, out_channels=16, kernel_size=2).double()
        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = torch.nn.Conv2d(in_channels=16, out_channels=64, kernel_size=3).double()
        self.fc1 = torch.nn.Linear(64 * 2 * 2, 128).double()
        self.fc2 = torch.nn.Linear(128, 64).double()
        self.fc3 = torch.nn.Linear(64, 2).double()
        
        self.softmax = torch.nn.Softmax(dim=-1)


        if state_dict_path is not None:
            self.load_state_dict(torch.load(state_dict_path))
            self.eval()

    
    def save_weights(self, state_dict_path):
        torch.save(self.state_dict(), state_dict_path)


    def forward(self, x):

        x = self.pool(F.relu(self.conv1(x)))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return self.softmax(x)

    def predict(self, x):

        return self.forward(x).detach().numpy()[0]


if __name__ == "__main__":

    tensor = torch.tensor(torch.from_numpy(np.random.rand(1, 2, 9, 9)), dtype=torch.double)

    model1 = UTTT_Model()

    print(model1.predict(tensor))
    # print(list(model1.parameters())[0][0])

    model1.save_weights("./ModelInstances/uttt_conv1_model")

    # model2 = UTTT_Model()

    # print(model2.forward(tensor))
    # # print(list(model2.parameters())[0][0])

    # model2.save_weights("./ModelInstances/uttt_conv1_model2")

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

