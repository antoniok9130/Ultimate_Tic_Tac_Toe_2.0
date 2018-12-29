
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

def getMoves(record):
    return [[int(record[i]), int(record[i+1])] for i in range(0, len(record), 2)]

class Supervised_Environment(UTTT_Environment):

    def __init__(self):
        super(Supervised_Environment, self).__init__()

    def get_action(self):
        self.i += 1
        return self.currentGame[self.i]

    def return_observation(self):
        return np.rot90(self.board if not self.flip else np.fliplr(self.board), k=self.rot), self.reward, self.done, {"legal": self.legal, "player": self.player}

    def additional_reset(self):
        if hasattr(self, "current"):
            self.current += 1
        else:
            with open("./Data/TrainingGames.txt") as file:
                self.games = [row.strip() for row in file]

            # self.games = list(set(self.games))
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




# 7:20 hrs as of 4:30pm
def train(num_episodes, explore_prob, average=100, **kwargs):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Training on:  ", device)

    # P1_model = UTTT_Model(verbose=True).to(device)
    # P2_model = UTTT_Model().to(device)
    # P1_trainer = Trainer(P1_model, device, **kwargs)
    # P2_trainer = Trainer(P2_model, device, **kwargs)

    model_instance_directory = "./Attempts/supervised1"
    sp.call(f"mkdir -p {model_instance_directory}", shell=True)

    with open(f"{model_instance_directory}/loss.csv", "w") as file:
        file.write(f"episode,loss\n")

    # try:
    #     model = UTTT_Model(f"{model_instance_directory}/most_recent_uttt_model", verbose=True).to(device)
    # except:
    model = UTTT_Model(verbose=True).to(device)
    
    trainer = Trainer(model, device, **kwargs)

    h, w = transform_image_shape

    # env = UTTT_Environment()
    env = Supervised_Environment()

    # P1_cumulative_rewards = []
    # P2_cumulative_rewards = []
    # P1_max_mean = 0
    # P2_max_mean = 0
    # cumulative_rewards = []
    losses = []
    for episode in range(num_episodes):
        if env.finished:
            break

        try:

            cumulative_reward = 0
            short_term = Memory(None, buckets=True)

            observation = env.reset()
            prev_states = [observation]
            action = env.random_action()
            observation, reward, done, info = env.step(action)
            prev_states.append(observation)
            observation, reward, done, info = env.step(get_second_move(*action))
            prev_states.append(observation)

            done = False
            timestep = 0
            player = N

            while not done and timestep <= 81:
                # print(f"Game: {game}      Iteration: {iteration}")
                # env.render() 

                # if np.random.random() < explore_prob*(num_episodes-episode)/num_episodes:
                #     action = env.random_action()
                # else:
                #     legal_moves = getLegalMovesField(env.quadrants, env.board, env.previousMove)
                #     # if player == P1:
                #     #     rewards = P2_model.predict(prev_state, device)
                #     # else:
                #     #     rewards = P1_model.predict(prev_state, device)
                #     rewards = model.predict(prev_states[-1], device)

                #     np.multiply(rewards+1, legal_moves, rewards)
                #     action = unflatten_move(argmax(rewards))

                observation, reward, done, info = env.step(env.get_action())
                del prev_states[0]
                prev_states.append(observation)

                if not info["legal"]:
                    printBoard(observation, env.quadrants)
                    print(action)
                    print(env.legalMoves)
                    raise Exception("Illegal Move")

                player = info["player"]
                cumulative_reward += reward
                
                short_term.remember([prev_states[-3], flatten_move(action), reward, done, observation])

                timestep += 1

            if timestep > 81 and not done:
                raise Exception("Invalid Game")

            
            # P1_short_term = Memory(None, buckets=True)
            # P2_short_term = Memory(None, buckets=True)

            discounted_reward_P1 = 0
            discounted_reward_P2 = 0
            for i in range(len(short_term)-1, -1, -1):
                short_term_reward = short_term[i][2] * (1 if i%2 == 0 else -1)

                discounted_reward_P1 = 0.95 * discounted_reward_P1 + short_term_reward
                discounted_reward_P2 = 0.95 * discounted_reward_P2 - short_term_reward

                if i%2 == 0:
                    short_term[i][2] = discounted_reward_P1
                    # P1_short_term.remember(short_term[i])
                else:
                    short_term[i][2] = discounted_reward_P2
                    # P2_short_term.remember(short_term[i])

            # print([x[2] for x in P1_short_term.memory])
            # print([x[2] for x in P2_short_term.memory])
            # print(discounted_reward_P1)
            # print(discounted_reward_P2)
            # exit(1)

            # P1_trainer.memory.remember(P1_short_term.memory)
            # P2_trainer.memory.remember(P2_short_term.memory)
            trainer.memory.remember(short_term.memory)

            print(f"\rEp: {episode}".ljust(15), end="")

                # file.write(f"{episode},{discounted_reward_P2},2\n")

            # P1_cumulative_rewards.append(discounted_reward_P1)
            # P2_cumulative_rewards.append(discounted_reward_P2)
            # cumulative_rewards.append(discounted_reward_P1)

            # P1_mean = np.mean(P1_cumulative_rewards[-average:])
            # P2_mean = np.mean(P2_cumulative_rewards[-average:])
            # mean = np.mean(cumulative_rewards[-average:])

            # print(f"  P1:  {round(P1_mean, 2)}".ljust(15), end="")
            # print(f"  P2:  {round(P2_mean, 2)}".ljust(15), end="")
            # print(f"  Mean:  {round(mean, 4)}".ljust(20), end="")
                # file.write(f"{episode},{P2_mean},2\n")

            # if discounted_reward_P1 > (P1_mean-0.5*np.std(P1_cumulative_rewards[-average:])):
            #     P1_trainer.memory.remember(P1_short_term.memory)

            # if discounted_reward_P2 > (P2_mean-0.5*np.std(P2_cumulative_rewards[-average:])):
            #     P2_trainer.memory.remember(P2_short_term.memory)

            # if P1_mean > P1_max_mean:
            #     P1_model.save_weights(f"{model_instance_directory}/P1_max_uttt_model")
            #     P1_max_mean = P1_mean

            # if P2_mean > P2_max_mean:
            #     P2_model.save_weights(f"{model_instance_directory}/P2_max_uttt_model")
            #     P2_max_mean = P2_mean

            # P1_trainer.experience_replay()
            # P2_trainer.experience_replay()
            loss = trainer.experience_replay()
            if loss is not None:
                losses.append(loss)
                mean = np.mean(losses[-average:])
                print(f"  Mean Loss:  {round(mean, 6)}".ljust(25), end="")
            
                with open(f"{model_instance_directory}/loss.csv", "a") as file:
                    file.write(f"{episode},{mean}\n")
                    

            if episode%100 == 0:
                model.save_weights(f"{model_instance_directory}/most_recent_uttt_model")
                del losses[:-average]

        except IndexError as e:
            # print("\n",e,"\n")
            # print(env.i, "\n")
            pass
    
    # P1_model.save_weights(f"{model_instance_directory}/P1_trained_uttt_model")
    # P2_model.save_weights(f"{model_instance_directory}/P2_trained_uttt_model")


    model.save_weights(f"{model_instance_directory}/most_recent_uttt_model")




if __name__ == "__main__":
    train(**{
        "learning_rate": 0.01,
        "momentum": 0.9,
        "milestones": [50000, 100000],
        "explore_prob": 0.25,
        "discount": 0.95,
        "max_memory_size": 1000,
        "batch_size": 50,
        "mini_batch_size": 32,
        "num_episodes": 250000
    })
            
