import sys
sys.path.append("../../")

import torch
import numpy as np

import time
from UTTT.utils import rot90, board_rot90, flatten_move, cartesian_move

class Memory():

    def __init__(self, max_memory_size, buckets=True, **kwargs):
        self.max_memory_size = max_memory_size
        self.buckets = buckets
        self.memory = []

    def __getitem__(self, i):
        return self.memory[i]

    def __len__(self):
        return len(self.memory)

    def remember(self, items):
        if self.buckets:
            self.memory.append(items)
        else:
            self.memory.extend(items)

        if self.max_memory_size is not None:
            excess = len(self.memory) - self.max_memory_size
            if excess > 0: del self.memory[:excess]

    def sample(self, num):
        if len(self.memory) > 0:
            indices = list(np.random.randint(len(self.memory), size=num))
            if not self.buckets:
                return [self.memory[i] for i in indices]
            else:
                indices = [(i, np.random.randint(len(self.memory[i]))) for i in indices]
                return [self.memory[i][j] for i, j in indices]

        return []


class BaseModel(torch.nn.Module):

    def __init__(self, max_size=None, buckets = True, 
                batch_size=1, mini_batch_size = 64, discount=0.95,
                verbose=False, 
                **kwargs):

        super(BaseModel, self).__init__()

    
    def load_weights(self, state_dict_path: str):
        self.load_state_dict(torch.load(state_dict_path))
        self.eval()

    def save_weights(self, state_dict_path: str):
        torch.save(self.state_dict(), state_dict_path)

    
    def conv_out_shape(self, input, kernel_size, stride, padding=0, **kwargs):
        c = 1 # input[0]
        h = (input[0]+2*padding-(kernel_size-1)-1)/stride+1
        w = (input[1]+2*padding-(kernel_size-1)-1)/stride+1
        if h%1 != 0:
            print(input, "->", (c, h, w))
            raise Exception("Height out is not an integer")
        if w%1 != 0:
            print(input, "->", (c, h, w))
            raise Exception("Width out is not an integer")
        return int(h), int(w)


    def transform(self, x):
        return np.array(x)


    def forward(self, x):
        return x


    def predict(self, x, device=None):
        if device is None:
            return self.forward(torch.tensor(torch.from_numpy(self.transform(x)), dtype=torch.double)).detach().numpy()
        else:
            return self.forward(torch.tensor(torch.from_numpy(self.transform(x)), dtype=torch.double).to(device)).cpu().detach().numpy()

        
        



class Trainer:

    def __init__(self, model, device, **kwargs):
        self.model = model
        self.device = device

        self.memory = Memory(**kwargs)
        self.init_trainer(**kwargs)
        self.init_batch(**kwargs)

    
    def init_trainer(self, learning_rate, milestones, momentum=0, policy_loss="CrossEntropyLoss", value_loss="MSELoss", **kwargs):
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=learning_rate, momentum=momentum)
        self.policy_criterion = getattr(torch.nn, policy_loss)()
        self.value_criterion = getattr(torch.nn, value_loss)()
        self.scheduler = torch.optim.lr_scheduler.MultiStepLR(self.optimizer, milestones=milestones)


    def init_batch(self, batch_size, mini_batch_size, discount=0.95, **kwargs):
        self.batch_size = batch_size
        self.mini_batch_size = mini_batch_size
        self.discount = discount

    
    def experience_replay(self, add_max=True):
        if len(self.memory) > 0:
            batches = []
            for _ in range(min(self.batch_size, len(self.memory))): # np.random.randint(1, 2)
                sample = self.memory.sample(self.mini_batch_size)

                batch_input = []
                policy_labels = []
                value_labels = []
                for state, action, reward in sample:

                    flip = True if np.random.randint(2) == 1 else False
                    k = np.random.randint(4)

                    batch_input.append(np.array(board_rot90(state, k=k, flip=flip)))

                    policy_labels.append(flatten_move(cartesian_move(rot90(action[0], action[1], k=k, flip=flip))))
                    value_labels.append([reward])

                    

                batches.append((self.model.transform(batch_input), np.array(policy_labels), np.array(value_labels)))
                
            if len(batches) > 0:
                self.scheduler.step()
                running_loss = 0
                for batch_input, policy_label, value_label in batches:
                    input_tensor = torch.from_numpy(batch_input).double().to(self.device)
                    policy_label_tensor = torch.from_numpy(policy_label).to(self.device)
                    value_label_tensor = torch.from_numpy(value_label).double().to(self.device)
            
                    self.optimizer.zero_grad()
                    policy, value = self.model.forward(input_tensor)
                    loss = self.policy_criterion(policy, policy_label_tensor)+\
                            self.value_criterion(value, value_label_tensor)
                    loss.backward()
                    self.optimizer.step()
                    running_loss += loss.item()

                    if running_loss > 1000000000:
                        print("Running Loss:  ", running_loss)
                        exit(1)

                return running_loss / len(batches)

            else:
                print("Batch is empty:", len(batches))

        else:
            print("Memory is empty:", len(self.memory))

        return None
                


current_time_milli = lambda: int(round(time.time() * 1000))