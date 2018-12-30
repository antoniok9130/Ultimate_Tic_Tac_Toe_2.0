import sys
sys.path.append("../../")

import numpy as np
from numba import jit
import torch
import torch.nn.functional as F

from Trainer import *
from UTTT import *

transform_image_shape = (9, 9)

model_input_size = 2
model_output_size = 81

# @jit(cache=True, nopython=True)
def transform_board(x):
    x = np.array(x)
    return np.array([x == P1, x == P2], dtype=np.bool_)

class UTTT_Model(BaseModel):

    def __init__(self, state_dict_path=None, verbose=False):

        super(UTTT_Model, self).__init__()

        input_shape = transform_image_shape
        if verbose: print("input:      ", input_shape)
        conv1_kernel = 3
        conv1_stride = 1
        conv1_out_channels = 16

        self.conv1 = torch.nn.Conv2d(in_channels=model_input_size, out_channels=conv1_out_channels, kernel_size=conv1_kernel, stride=conv1_stride).double()

        conv1_output_shape = self.conv_out_shape(input_shape, conv1_kernel, conv1_stride)
        if verbose: print("conv1 out:  ", conv1_output_shape)
        conv2_kernel = 3
        conv2_stride = 1
        conv2_out_channels = 32

        self.conv2 = torch.nn.Conv2d(in_channels=conv1_out_channels, out_channels=conv2_out_channels, kernel_size=conv2_kernel, stride=conv2_stride).double()

        h, w = self.conv_out_shape(conv1_output_shape, conv2_kernel, conv2_stride)
        if verbose: print("conv2 out:  ", (h, w))

        self.view_size = h*w*conv2_out_channels
        if verbose: print("view size:  ", self.view_size)
        
        self.fc1 = torch.nn.Linear(self.view_size, 256).double()
        self.fc2 = torch.nn.Linear(256, model_output_size).double()

        if state_dict_path is not None:
            self.load_weights(state_dict_path)

    def transform(self, x):
        return np.reshape(np.array(x, dtype=np.double), (-1, model_input_size, transform_image_shape[0], transform_image_shape[1])).astype(np.double)

    def forward(self, x):

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, self.view_size)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return x


if __name__ == "__main__":
    model = UTTT_Model(verbose=True)