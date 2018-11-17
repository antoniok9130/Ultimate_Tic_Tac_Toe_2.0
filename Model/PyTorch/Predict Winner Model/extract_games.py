
with open("../ModelInstances/predict3/log.csv") as log, open("../ModelInstances/predict3/games.txt", "w") as out:
    # next(log)
    for row in log:
        out.write(row.split(",")[5]+"\n")

