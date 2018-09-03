//
// Created by Antonio on 2018-04-18.
//

#ifndef ULTIMATE_TIC_TAC_TOE_ZERO_GAME_V2_1_H
#define ULTIMATE_TIC_TAC_TOE_ZERO_GAME_V2_1_H

#include "memory"
#include "board.h"

class Node;

Move getMoveV2_1(Node* node, double duration = 3.0);

Move getChildVisitedMostV2_1(Node* node);
std::unique_ptr<Node>& getChildHighestUCTV2_1(Node* node);

void selectV2_1(Node* node);
void expandV2_1(Node* node);
int runSimulationV2_1(Node* node);
void backpropogateV2_1(Node* node, int winner);

#endif  // ULTIMATE_TIC_TAC_TOE_ZERO_GAME_V2_1_H