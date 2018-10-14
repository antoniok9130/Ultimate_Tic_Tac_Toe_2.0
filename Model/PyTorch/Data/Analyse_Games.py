import operator

analyzed = [[{} for j in range(9)] for i in range(9)]
games = []

with open("RecordedGames.txt") as file:
    for row in file:
        games.append(row.strip())
        moves = [int(e) for e in row.strip()]
        g = moves[0]
        l = moves[1]        
    
        pair = (moves[2], moves[3])

        if pair in analyzed[g][l]:
            analyzed[g][l][pair][0] += 1

        else:
            analyzed[g][l][pair] = [1, {}]

for i in range(9):
    for j in range(9):
        # analyzed[i][j] = sorted(analyzed[i][j].items(), key=operator.itemgetter(1), reverse=True)
        print(f"({i}, {j}):   [{', '.join([f'{key}: {val[0]}' for key, val in analyzed[i][j].items()])}]")


games = [x for x in games if games.count(x) > 1]

if len(games) > 0:
    print("There are ", int(len(games)/2), " duplicate games:")
    for game in games:
        print("   ", game)
else:
    print("There are no duplicate games")
