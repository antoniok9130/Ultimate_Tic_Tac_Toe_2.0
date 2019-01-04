import sys
sys.path.append("../../")

import numpy as np
from numba import jit
import torch
import torch.nn.functional as F

from Trainer import *
from UTTT import *

transform_image_shape = (9, 9)

# @jit(cache=True, nopython=True)
def transform_board(x):
    x = np.array(x)
    return np.array([x == P1, x == P2], dtype=np.bool_)

class UTTT_Model(BaseModel):

    def __init__(self, state_dict_path=None, verbose=False):

        super(UTTT_Model, self).__init__()

        conv1_params = {
            "in_channels": 2,
            "out_channels": 16,
            "kernel_size": 3,
            "stride": 1,
            "padding": 1
        }
        self.conv1 = torch.nn.Conv2d(**conv1_params).double()
        self.model_input_size = conv1_params["in_channels"]
        conv1_output_shape = self.conv_out_shape(transform_image_shape, **conv1_params)


        conv2_params = {
            "in_channels": conv1_params["out_channels"],
            "out_channels": 32,
            "kernel_size": 3,
            "stride": 1,
            "padding": 1
        }
        self.conv2 = torch.nn.Conv2d(**conv2_params).double()
        conv2_output_shape = self.conv_out_shape(conv1_output_shape, **conv2_params)


        policy_conv_params = {
            "in_channels": conv2_params["out_channels"],
            "out_channels": 2,
            "kernel_size": 1,
            "stride": 1
        }
        self.policy_conv = torch.nn.Conv2d(**policy_conv_params).double()
        policy_conv_output_shape = self.conv_out_shape(conv2_output_shape, **policy_conv_params)

        policy_fc_params = {
            "in_features": product(policy_conv_output_shape)*policy_conv_params["out_channels"],
            "out_features": 81
        }
        self.policy_viewsize = policy_fc_params["in_features"]
        self.policy_fc = torch.nn.Linear(**policy_fc_params).double()


        value_conv_params = {
            "in_channels": conv2_params["out_channels"],
            "out_channels": 1,
            "kernel_size": 1,
            "stride": 1
        }
        self.value_conv = torch.nn.Conv2d(**value_conv_params).double()
        value_conv_output_shape = self.conv_out_shape(conv2_output_shape, **value_conv_params)

        value_fc1_params = {
            "in_features": product(value_conv_output_shape)*value_conv_params["out_channels"],
            "out_features": 64
        }
        self.value_viewsize = value_fc1_params["in_features"]
        self.value_fc1 = torch.nn.Linear(**value_fc1_params).double()

        value_fc2_params = {
            "in_features": value_fc1_params["out_features"],
            "out_features": 1
        }
        self.value_fc2 = torch.nn.Linear(**value_fc2_params).double()


        if state_dict_path is not None:
            self.load_weights(state_dict_path)


        if verbose:
            amt = 25
            print("input:".ljust(amt), transform_image_shape)
            print("conv1 out:".ljust(amt), conv1_output_shape, conv1_params["out_channels"])
            print("conv2 out:".ljust(amt), conv2_output_shape, conv2_params["out_channels"])
            print("policy conv out:".ljust(amt), policy_conv_output_shape)
            print("policy view size:".ljust(amt), policy_fc_params["in_features"])
            print("value conv out:".ljust(amt), value_conv_output_shape)
            print("value view size:".ljust(amt), value_fc1_params["in_features"])

    def transform(self, x):
        return np.reshape(np.array(x, dtype=np.double), (-1, self.model_input_size, transform_image_shape[0], transform_image_shape[1]))

    def forward(self, x):

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))

        policy = F.relu(self.policy_conv(x))
        policy = self.policy_fc(policy.view(-1, self.policy_viewsize))

        value = F.relu(self.value_conv(x))
        value = self.value_fc1(value.view(-1, self.value_viewsize))
        value = self.value_fc2(value)
        value = torch.tanh(value)

        return policy, value


    def predict(self, x, device=None, preprocess=False):
        if preprocess:
            x = transform_board(x)
        if device is None:
            policy, value = self.forward(torch.tensor(torch.from_numpy(self.transform(x)), dtype=torch.double))
            policy = policy.detach().numpy()[0]
            value = value.detach().numpy()[0]
        else:
            policy, value = self.forward(torch.tensor(torch.from_numpy(self.transform(x)), dtype=torch.double).to(device))
            policy = policy.cpu().detach().numpy()[0]
            value = value.cpu().detach().numpy()[0]

        return policy, value


if __name__ == "__main__":
    model = UTTT_Model(verbose=True)
    print(model)
    # model.save_weights("./Attempts/test.pt")