import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./supervised4/loss.csv")

# df = df[df["player"] == 1]
# P2_df = df[df["player"] == 2]

# print(df.groupby("winner").count())

# data.sort_values("iteration")

# print(df[[f"accuracy__{length}" for length in lengths]].mean(axis=1).idxmax())
field = "loss"
print(df[field].max())
print(df[field].idxmax())
print(df[field].min())
print(df[field].idxmin())
# print(df['game'].nunique(), " ?= ",df['game'].count())

# df["game_length"] = df["game"].apply(lambda x: len(x)/2)
# df[["iteration", "game_length"]].plot(x="iteration")
# df[["iteration", "duration"]].plot(x="iteration")
# for i, length in enumerate(lengths):
# df = df[df["iteration"] > 500]
plt.plot(df["episode"], df[field], c=f"C0")
plt.plot(df["episode"], np.polyval(np.polyfit(df["episode"], df[field], 1), df["episode"]), c=f"C1", label=field)

    # plt.plot(df["iteration"], df[f"accuracy__{length}"], c=f"C{i}", label=f"accuracy__{length}")
    # plt.plot(df["iteration"], np.polyval(np.polyfit(df["iteration"], df[f"accuracy__{length}"], 1), df["iteration"]))
plt.show()

# total_length = 0
# num_games = 0
# with open("../ModelInstances/predict3/games.txt") as file:
#     for row in file:
#         total_length += len(row.strip())/2
#         num_games += 1

# print(total_length/num_games)