
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

    P1_model = UTTT_Model(verbose=True).to(device)
    P2_model = UTTT_Model().to(device)
    P1_trainer = Trainer(P1_model, device, **kwargs)
    P2_trainer = Trainer(P2_model, device, **kwargs)

    model_instance_directory = "./Attempts/attempt3"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)

    with open(f"{model_instance_directory}/rewards.csv", "w") as file:
        file.write(f"episode,cumulative_reward,player\n")
    with open(f"{model_instance_directory}/mean_rewards.csv", "w") as file:
        file.write(f"episode,cumulative_reward,player\n")

    h, w = transform_image_shape

    env = UTTT_Environment()

    P1_cumulative_rewards = []
    P2_cumulative_rewards = []
    P1_max_mean = 0
    P2_max_mean = 0
    for episode in range(num_episodes):

        cumulative_reward = 0
        short_term = Memory(None, buckets=True)

        action = env.random_action()
        observation = env.reset()
        done = False
        timestep = 0
        player = N

        while not done and timestep <= 81:
            # print(f"Game: {game}      Iteration: {iteration}")
            # env.render()

            prev_state = observation

            if np.random.random() < explore_prob*(num_episodes-episode)/num_episodes:
                action = env.random_action()
            else:
                legal_moves = getLegalMovesField(env.quadrants, env.board, env.previousMove)
                if player == P1:
                    rewards = P2_model.predict(prev_state, device)
                else:
                    rewards = P1_model.predict(prev_state, device)

                np.multiply(rewards, legal_moves, rewards)
                action = unflatten_move(argmax(rewards))

            observation, reward, done, info = env.step(action)
            if not info["legal"]:
                printBoard(observation, env.quadrants)
                print(action)
                print(rewards)
                print(env.legalMoves)
                raise Exception("Illegal Move")

            player = info["player"]
            cumulative_reward += reward
            
            short_term.remember([prev_state, flatten_move(action), reward, done, observation])

            timestep += 1

        if timestep > 81 and not done:
            raise Exception("Invalid Game")

        
        P1_short_term = Memory(None, buckets=True)
        P2_short_term = Memory(None, buckets=True)

        discounted_reward_P1 = 0
        discounted_reward_P2 = 0
        for i in range(len(short_term)-1, -1, -1):
            short_term_reward = short_term[i][2] * (1 if i%2 == 0 else -1)

            discounted_reward_P1 = 0.95 * discounted_reward_P1 + short_term_reward
            discounted_reward_P2 = 0.95 * discounted_reward_P2 - short_term_reward

            if i%2 == 0:
                short_term[i][2] = discounted_reward_P1
                P1_short_term.remember(short_term[i])
            else:
                short_term[i][2] = discounted_reward_P2
                P2_short_term.remember(short_term[i])

        # print([x[2] for x in P1_short_term.memory])
        # print([x[2] for x in P2_short_term.memory])
        # print(discounted_reward_P1)
        # print(discounted_reward_P2)
        # exit(1)

        P1_trainer.memory.remember(P1_short_term.memory)
        P2_trainer.memory.remember(P2_short_term.memory)

        print(f"\rEp: {episode}".ljust(15), end="")

        with open(f"{model_instance_directory}/rewards.csv", "a") as file:
            file.write(f"{episode},{discounted_reward_P1},1\n")
            file.write(f"{episode},{discounted_reward_P2},2\n")

        P1_cumulative_rewards.append(discounted_reward_P1)
        P2_cumulative_rewards.append(discounted_reward_P2)

        P1_mean = np.mean(P1_cumulative_rewards[-average:])
        P2_mean = np.mean(P2_cumulative_rewards[-average:])

        print(f"  P1:  {round(P1_mean, 2)}".ljust(15), end="")
        print(f"  P2:  {round(P2_mean, 2)}".ljust(15), end="")
        with open(f"{model_instance_directory}/mean_rewards.csv", "a") as file:
            file.write(f"{episode},{P1_mean},1\n")
            file.write(f"{episode},{P2_mean},2\n")

        # if discounted_reward_P1 > (P1_mean-0.5*np.std(P1_cumulative_rewards[-average:])):
        #     P1_trainer.memory.remember(P1_short_term.memory)

        # if discounted_reward_P2 > (P2_mean-0.5*np.std(P2_cumulative_rewards[-average:])):
        #     P2_trainer.memory.remember(P2_short_term.memory)

        if P1_mean > P1_max_mean:
            P1_model.save_weights(f"{model_instance_directory}/P1_max_uttt_model")
            P1_max_mean = P1_mean

        if P2_mean > P2_max_mean:
            P2_model.save_weights(f"{model_instance_directory}/P2_max_uttt_model")
            P2_max_mean = P2_mean

        P1_trainer.experience_replay()
        P2_trainer.experience_replay()
    
    P1_model.save_weights(f"{model_instance_directory}/P1_trained_uttt_model")
    P2_model.save_weights(f"{model_instance_directory}/P2_trained_uttt_model")




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
        "num_episodes": 15000
    })
            
