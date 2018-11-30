import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

lengths = ["0_15", "15_30", "30_45", "45_60", "60_"]
df = pd.read_csv("../ModelInstances/predict8/log.csv")

# print(df.groupby("winner").count())

# data.sort_values("iteration")

print(df[[f"accuracy__{length}" for length in lengths]].mean(axis=1).idxmax())
print(df[[f"loss__{length}" for length in lengths]].mean(axis=1).idxmin())
# print(df['game'].nunique(), " ?= ",df['game'].count())

# df["game_length"] = df["game"].apply(lambda x: len(x)/2)
# df[["iteration", "game_length"]].plot(x="iteration")
# df[["iteration", "duration"]].plot(x="iteration")
# for i, length in enumerate(lengths):
#     plt.plot(df["iteration"], df[f"loss__{length}"], c=f"C{i}")
#     plt.plot(df["iteration"], np.polyval(np.polyfit(df["iteration"], df[f"loss__{length}"], 1), df["iteration"]), c=f"C{i}", label=f"loss__{length}")

    # plt.plot(df["iteration"], df[f"accuracy__{length}"], c=f"C{i}", label=f"accuracy__{length}")
    # plt.plot(df["iteration"], np.polyval(np.polyfit(df["iteration"], df[f"accuracy__{length}"], 1), df["iteration"]))
# plt.show()

# total_length = 0
# num_games = 0
# with open("../ModelInstances/predict3/games.txt") as file:
#     for row in file:
#         total_length += len(row.strip())/2
#         num_games += 1

# print(total_length/num_games)