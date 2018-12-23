
import sys
sys.path.append("../../")

import os
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


def train(num_episodes, explore_prob, average=100, **kwargs):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = UTTT_Model(verbose=True).to(device)
    trainer = Trainer(model, device, **kwargs)

    model_instance_directory = "./Attempts/attempt1"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)

    with open(f"{model_instance_directory}/rewards.csv", "w") as file:
        file.write(f"episode,cumulative_reward\n")
    with open(f"{model_instance_directory}/mean_rewards.csv", "w") as file:
        file.write(f"episode,cumulative_reward\n")

    h, w = transform_image_shape

    env = UTTT_Environment()

    cumulative_rewards = []
    max_mean = 0
    for episode in range(num_episodes):

        cumulative_reward = 0
        short_term = Memory(None, buckets=True)

        action = env.random_action()
        observation = env.reset()
        done = False
        timestep = 0

        while not done and timestep <= 81:
            # print(f"Game: {game}      Iteration: {iteration}")
            # env.render()

            prev_state = observation

            if np.random.random() < explore_prob*(num_episodes-episode)/num_episodes:
                action = env.random_action()
            else:
                legal_moves = getLegalMovesField(env.quadrants, env.board, env.previousMove)
                rewards = model.predict(prev_state, device)
                np.multiply(rewards, legal_moves, rewards)
                action = argmax(rewards)
                action = [int(action//9), int(action%9)]

            observation, reward, done, info = env.step(action)
            if not info["legal"]:
                printBoard(observation, env.quadrants)
                print(action)
                print(rewards)
                print(env.legalMoves)
                raise Exception("Illegal Move")

            cumulative_reward += reward

            short_term.remember([prev_state, flatten_move(action), reward, done, observation])

            timestep += 1

        if timestep > 81 and not done:
            raise Exception("Invalid Game")

        discounted_reward_P1 = 0
        discounted_reward_P2 = 0
        for i in range(len(short_term)-1, -1, -1):
            short_term_reward = short_term[i][2] * (1 if i%1 == 0 else -1)

            discounted_reward_P1 = 0.95 * discounted_reward_P1 + short_term_reward
            discounted_reward_P2 = 0.95 * discounted_reward_P2 - short_term_reward

            short_term[i][2] = discounted_reward_P1 if i%1 == 0 else discounted_reward_P2

        print(f"\rEpisode: {episode}".ljust(20), end="")

        with open(f"{model_instance_directory}/rewards.csv", "a") as file:
            file.write(f"{episode},{cumulative_reward}\n")

        cumulative_rewards.append(cumulative_reward)
        remember = True
        mean = np.mean(cumulative_rewards[-average:])
        print(f"  Mean:  {round(mean, 4)}".ljust(20), end="")
        with open(f"{model_instance_directory}/mean_rewards.csv", "a") as file:
            file.write(f"{episode},{mean}\n")

        if cumulative_reward < (mean-0.5*np.std(cumulative_rewards[-average:])):
            remember = False

        if mean > max_mean:
            model.save_weights(f"{model_instance_directory}/max_uttt_model")
            max_mean = mean

        if remember:
            trainer.memory.remember(short_term.memory)

        loss = trainer.experience_replay()
    
    model.save_weights(f"{model_instance_directory}/trained_uttt_model")




if __name__ == "__main__":
    train(**{
        "learning_rate": 0.001,
        "momentum": 0.9,
        "weight_decay": 0.0001,
        "explore_prob": 0.15,
        "discount": 0.95,
        "max_memory_size": 300,
        "batch_size": 50,
        "mini_batch_size": 32,
        "num_episodes": 10000
    })
            
