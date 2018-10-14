import operator

analyzed = [[{} for j in range(9)] for i in range(9)]

with open("RecordedGames.txt") as file:
    for row in file:
        moves = [int(e) for e in row.strip()]
        g = moves[0]
        l = moves[1]        
    
        pair = (moves[2], moves[3])

        if pair in analyzed[g][l]:
            analyzed[g][l][pair] += 1

        else:
            analyzed[g][l][pair] = 1

for i in range(9):
    for j in range(9):
        analyzed[i][j] = sorted(analyzed[i][j].items(), key=operator.itemgetter(1), reverse=True)
        print(f"({i}, {j}):  ", analyzed[i][j])
