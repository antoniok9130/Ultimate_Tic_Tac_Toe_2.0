import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../ModelInstances/predict3/log.csv")

# print(df.groupby("winner").count())

# data.sort_values("iteration")

print(df['accuracy'].idxmax())
print(df['loss'].idxmin())
# print(df['game'].nunique(), " ?= ",df['game'].count())

# df[["iteration", "loss", "accuracy"]].plot(x="iteration")
df["game_length"] = df["game"].apply(lambda x: len(x)/2)
df[["iteration", "game_length"]].plot(x="iteration")
# df[["iteration", "duration"]].plot(x="iteration")
plt.show()

# total_length = 0
# num_games = 0
# with open("../ModelInstances/predict3/games.txt") as file:
#     for row in file:
#         total_length += len(row.strip())/2
#         num_games += 1

# print(total_length/num_games)