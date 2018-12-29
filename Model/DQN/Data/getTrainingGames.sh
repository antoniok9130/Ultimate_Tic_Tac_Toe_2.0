#!/bin/bash
# wc -l ../../PyTorch/Data/TrainingGames.txt
# wc -l ../../../Game/C++/MCTS_V2.5/record23.txt
# wc -l ../../../Game/C++/MCTS_V2.5/record24.txt
# wc -l ../../../Game/C++/MCTS_V2.5/record25.txt
# wc -l ../../../Game/C++/MCTS_V2.5/record26.txt

# dos2unix ../../PyTorch/Data/TrainingGames.txt
# head -1 ../../PyTorch/Data/TrainingGames.txt | xxd
# head -2 ../../../Game/C++/MCTS_V2.5/record23.txt | xxd

cat ../../PyTorch/Data/TrainingGames.txt > ./TrainingGames.txt
cat ../../../Game/C++/MCTS_V2.5/record23.txt >> ./TrainingGames.txt
cat ../../../Game/C++/MCTS_V2.5/record24.txt >> ./TrainingGames.txt
cat ../../../Game/C++/MCTS_V2.5/record25.txt >> ./TrainingGames.txt
cat ../../../Game/C++/MCTS_V2.5/record26.txt >> ./TrainingGames.txt