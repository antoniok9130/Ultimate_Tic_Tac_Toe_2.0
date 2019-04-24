#ifndef __MCTS_H__
#define __MCTS_H__

#include "state.h"

bool check2InRow(const unsigned int& quadrant, const int& position);
// bool check2InRowSwitch(const unsigned int& quadrant, const int& position);

void getMCTSMove(State* s, int& global, int& local, const unsigned int& numIterations = 2000000);

bool isWin(State* s, int& global, int& local);

void select(State* s);
void expand(State* s);
int simulate(State* s);
void backpropogate(State* s);

#endif // __MCTS_H__
