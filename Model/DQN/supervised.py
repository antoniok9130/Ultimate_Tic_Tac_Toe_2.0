
import sys
sys.path.append("../../")

import os
import subprocess as sp
from math import inf
import time
from random import shuffle

import numpy as np
import torch
import torch.nn.functional as F
from math import ceil

from Trainer import *
from Model import *
from UTTT import *
from Environment import *
from train import *

def getMoves(record):
    return [[int(record[i]), int(record[i+1])] for i in range(0, len(record), 2)]


class Supervised_Environment(UTTT_Environment):

    def __init__(self):
        super(Supervised_Environment, self).__init__()

    def get_action(self, model, device):
        self.i += 1
        g, l = self.currentGame[self.i][0], self.currentGame[self.i][1]
        return rot90(g, l, k=self.rot, flip=self.flip)

    def return_observation(self):
        return self.board, self.reward, self.done, {"legal": self.legal}

    def additional_reset(self):
        if hasattr(self, "current"):
            self.current += 1
        else:
            with open("./Data/TrainingGames.txt") as file:
                self.games = [row.strip() for row in file]

            print("Num Games:        ", len(self.games))
            self.games = list(set(self.games))
            print("Num Unique Games: ", len(self.games))
            shuffle(self.games)
            self.current = 0
            self.flip = False
            self.rot = 0

        if self.current >= len(self.games):
            shuffle(self.games)
            self.current = 0
            self.rot += 1
            if self.rot > 3:
                self.rot = 0
                if self.flip:
                    self.finished = True
                else:
                    self.flip = True

        self.currentGame = getMoves(self.games[self.current])
        self.i = -1


if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = UTTT_Model(verbose=True).to(device)
    
    train(**{
        "model_instance_directory": "./Attempts/supervised5",
        "model": model,
        "device": device,
        "environment": Supervised_Environment,
        
        "learning_rate": 0.01,
        "momentum": 0.9,
        "milestones": [90000, 180000],
        "discount": 0.95,
        "max_memory_size": 1500,
        "batch_size": 50,
        "mini_batch_size": 32,
        "num_episodes": 300000
    })
            
