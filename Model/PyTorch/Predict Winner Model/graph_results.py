import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../ModelInstances/predict3/log.csv")

# print(df.groupby("winner").count())

# data.sort_values("iteration")

print(df['accuracy'].idxmax())
print(df['loss'].idxmin())
print(df['game'].nunique(), " ?= ",df['game'].count())

df[["iteration", "loss", "accuracy"]].plot(x="iteration")
# df[["iteration", "duration"]].plot(x="iteration")
plt.show()