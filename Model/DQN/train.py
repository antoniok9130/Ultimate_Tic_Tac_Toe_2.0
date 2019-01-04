
import sys
sys.path.append("../../")

import os
import traceback
import subprocess as sp
from math import inf
import time

import numpy as np
import torch
import torch.nn.functional as F
from math import ceil

from Trainer import *
from Model import *
from UTTT import *
from Environment import *


def train(model_instance_directory, model, device, num_episodes, explore_prob, 
          environment=UTTT_Environment, average=100, **kwargs):

    # P1_model = UTTT_Model(verbose=True).to(device)
    # P2_model = UTTT_Model().to(device)
    # P1_trainer = Trainer(P1_model, device, **kwargs)
    # P2_trainer = Trainer(P2_model, device, **kwargs)
    
    trainer = Trainer(model, device, **kwargs)

    sp.call(f"mkdir -p {model_instance_directory}", shell=True)
    with open(f"{model_instance_directory}/loss.csv", "w") as file:
        file.write(f"episode,loss\n")


    h, w = transform_image_shape

    env = environment()

    losses = []
    times = []
    begin = current_time_milli()
    episode = 0
    while episode < num_episodes:
        start = current_time_milli()
        
        if env.finished:
            break

        try:
            env.reset()

            done = False
            timestep = 0

            observations = []
            
            # model = trainer.model.cpu()
            while not done and timestep <= 81:
                # env.render()
                action = env.get_action(trainer.model, device)
                
                observation, reward, done, info = env.step(action)
                if not done:
                    observations.append(transform_board(observation))
                timestep += 1
                
                if not info["legal"]:
                    quadrant = env.node.buildQuadrant()
                    printBoard(observation, quadrant)
                    print(getLegalMovesField(quadrant, observation, env.moves[-1]))
                    print(getLegalMoves1D(quadrant, observation, env.moves[-1]))
                    print(getLegalMoves2D(quadrant, observation, env.moves[-1]))
                    print(env.moves[-1])
                    print(action)
                    raise Exception("Illegal Move")

            if timestep > 81 and not done:
                raise Exception("Invalid Game")


            short_term = Memory(None, buckets=True)

            current = env.node.parent
            reward = 1
            for action, observation in zip(reversed(env.moves[2:]), reversed(observations)):
                reward = abs(reward-1)
                # short_term.remember([observation, current.get_priorities(), reward])
                short_term.remember([observation, flatten_move(action), reward])
                current = current.parent
            
            trainer.memory.remember(short_term.memory)


            print(f"\rEp: {episode}".ljust(15), end="")
            loss = trainer.experience_replay()

            if loss is not None:
                losses.append(loss)
                mean = np.mean(losses[-average:])
                print(f"  Mean Loss:  {round(mean, 6)}".ljust(25), end="")
            
                with open(f"{model_instance_directory}/loss.csv", "a") as file:
                    file.write(f"{episode},{mean}\n")

            episode += 1

            if episode%100 == 0:
                model.save_weights(f"{model_instance_directory}/most_recent_uttt_model")
                del losses[:-average]
                print(f"  Time:  {round(np.mean(times[-average:]), 6)}".ljust(25), end="")
                del times[:-average]

        except Exception as e:
            printBoard(observation, env.node.buildQuadrant())
            print(env.moves[-1])
            print(action)
            raise(e)
            # print(e)
            # exit(1)

        end = current_time_milli()
        times.append((end-start)/1000.0)

    model.save_weights(f"{model_instance_directory}/most_recent_uttt_model")

    print("\nTook", (current_time_milli()-begin)/1000.0, "seconds to train model")


if __name__ == "__main__":
    # try:
    #     model = UTTT_Model(f"{model_instance_directory}/most_recent_uttt_model", verbose=True).to(device)
    # except:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = UTTT_Model(verbose=True).to(device)

    train(**{
        "model_instance_directory": "./Attempts/attempt5",
        "model": model,
        "device": device,

        "learning_rate": 0.01,
        "momentum": 0.9,
        "milestones": [125000, 250000],
        "explore_prob": 0.25,
        "discount": 0.95,
        "max_memory_size": 1500,
        "batch_size": 50,
        "mini_batch_size": 32,
        "num_episodes": 500000
    })
            
