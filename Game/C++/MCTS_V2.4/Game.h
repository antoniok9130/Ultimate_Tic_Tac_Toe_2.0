//
// Created by Antonio on 2018-04-18.
//

#ifndef ULTIMATE_TIC_TAC_TOE_ZERO_GAME_H
#define ULTIMATE_TIC_TAC_TOE_ZERO_GAME_H

#include "Board.h"
#include "memory"

class Node;

Move getMove(Node* node, double duration = 3.0);

Move getChildVisitedMost(Node* node);
std::unique_ptr<Node>& getChildHighestUCT(Node* node);

void select(Node* node);
void expand(Node* node);
int runSimulation(Node* node);
void backpropogate(Node* node, int winner);

extern "C" {
void MCTS_select(Node* node);
void MCTS_expand(Node* node);
int MCTS_runSimulation(Node* node);
void MCTS_backpropogate(Node* node, int winner);
}

#endif  // ULTIMATE_TIC_TAC_TOE_ZERO_GAME_H