
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

def get_model_actions(model, observations, envs, explore_prob):
    if np.random.random() < explore_prob:
        return [env.random_action() for env in envs]
    else:
        legal_moves = [getLegalMovesField(env.quadrants, env.board, env.previousMove) for env in envs]
        rewards = model.predict(observations, device)
        return [unflatten_move(argmax(np.multiply(reward+1, legal_move))) for reward, legal_move in zip(rewards, legal_moves)]

def modify_envs(envs):
    pass


def train(model_instance_directory, model, device, num_episodes, explore_prob, 
          environment=UTTT_Environment, num_envs=1, get_actions=get_model_actions, modify_envs=modify_envs,
          average=100, **kwargs):

    # P1_model = UTTT_Model(verbose=True).to(device)
    # P2_model = UTTT_Model().to(device)
    # P1_trainer = Trainer(P1_model, device, **kwargs)
    # P2_trainer = Trainer(P2_model, device, **kwargs)
    
    trainer = Trainer(model, device, **kwargs)

    sp.call(f"mkdir -p {model_instance_directory}", shell=True)
    with open(f"{model_instance_directory}/loss.csv", "w") as file:
        file.write(f"episode,loss\n")


    h, w = transform_image_shape

    # env = environment()
    envs = [environment() for i in range(num_envs)]
    modify_envs(envs)

    losses = []
    times = []
    begin = current_time_milli()
    episode = 0
    while episode < num_episodes:
        start = current_time_milli()

        envs = [env for env in envs if not env.finished]

        if len(envs) < 1:
            break

        try:

            # cumulative_reward = 0
            short_terms = [Memory(None, buckets=True) for i in range(len(envs))]

            observations = [env.reset() for env in envs]
            observations = list(map(transform_board, observations))

            dones = [False for i in range(len(envs))]
            timesteps = [0 for i in range(len(envs))]
            active = [True for i in range(len(envs)) if dones[i] == False and timesteps[i] <= 81]

            while any(a for a in active):
                # env.render() 
                prev_states = [observations[i] for i in range(len(envs)) if active[i]]
                actions = get_actions(model, prev_states, [envs[i] for i in range(len(envs)) if active[i]], explore_prob*(num_episodes-episode)/num_episodes)

                prev_states = iter(prev_states)
                actions = iter(actions)
                for i in range(len(envs)):
                    if active[i]:
                        prev_state = next(prev_states)
                        action = next(actions)

                        observation, reward, done, info = envs[i].step(action)
                        observations[i] = transform_board(observation)
                        dones[i] = done
                        timesteps[i] += 1
                        active[i] = dones[i] == False and timesteps[i] <= 81

                        if not info["legal"]:
                            printBoard(observation)
                            print(action)
                            print(envs[i].legalMoves)
                            raise Exception("Illegal Move")

                        if timesteps[i] > 81 and not dones[i]:
                            raise Exception("Invalid Game")

                        short_terms[i].remember([prev_state, flatten_move(action), reward, done, observations[i]])

            for short_term in short_terms:
                reward_P1 = 1 if len(short_term)%2 == 1 else -1
                reward_P2 = 1 if len(short_term)%2 == 0 else -1
                for i in range(len(short_term)-1, -1, -1):
                    if i%2 == 0:
                        short_term[i][2] = reward_P1
                    else:
                        short_term[i][2] = reward_P2

                trainer.memory.remember(short_term.memory)

                print(f"\rEp: {episode}".ljust(15), end="")
                loss = trainer.experience_replay(add_max=False)

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

        except IndexError as e:
            pass

        end = current_time_milli()
        times.append((end-start)/(1000.0*num_envs))
        print(f"  Time:  {round(np.mean(times[-100:]), 6)}".ljust(25), end="")

    model.save_weights(f"{model_instance_directory}/most_recent_uttt_model")

    print("\nTook", (current_time_milli()-begin)/1000.0, "seconds to train model")


if __name__ == "__main__":
    # try:
    #     model = UTTT_Model(f"{model_instance_directory}/most_recent_uttt_model", verbose=True).to(device)
    # except:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    model = UTTT_Model("./Attempts/supervised3/most_recent_uttt_model", verbose=True).to(device)

    train(**{
        "model_instance_directory": "./Attempts/attempt4",
        "model": model,
        "device": device,

        "learning_rate": 0.01,
        "momentum": 0.9,
        "milestones": [125000, 250000],
        "explore_prob": 0.25,
        "discount": 0.95,
        "max_memory_size": 1000,
        "batch_size": 50,
        "mini_batch_size": 32,
        "num_episodes": 500000,
        "num_envs": 128
    })
            
