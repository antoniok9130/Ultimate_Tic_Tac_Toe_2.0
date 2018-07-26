//
// Created by Antonio on 2018-04-18.
//

#ifndef ULTIMATE_TIC_TAC_TOE_ZERO_GAME_H
#define ULTIMATE_TIC_TAC_TOE_ZERO_GAME_H

#include "memory"
#include "../Boards/board.h"

class Node;

std::unique_ptr<Node>& getMove(Node* node, double time = 2.5);

std::unique_ptr<Node>& getChildVisitedMost(Node* node);
std::unique_ptr<Node>& getChildHighestUCT(Node* node);

void select(Node* node);
void expand(Node* node);
int runSimulation(Node* node);
void backpropogate(Node* node, int winner);

#endif  // ULTIMATE_TIC_TAC_TOE_ZERO_GAME_H
