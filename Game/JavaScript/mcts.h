#ifndef __MCTS_H__
#define __MCTS_H__

#include "state.h"
// #define CHECK_DEPTH

// bool check2InRow(const unsigned int& quadrant, const int& position);
// bool check2InRowSwitch(const unsigned int& quadrant, const int& position);

void getMCTSMove(State* s, int& global, int& local, const unsigned int& numIterations = 2000000);

bool isWin(State* s, int& global, int& local);

#ifdef CHECK_DEPTH
void select(State* s, int depth);
#else
void select(State* s);
#endif

#ifdef CHECK_DEPTH
void expand(State* s, int depth);
#else
void expand(State* s);
#endif

int simulate(State* s);
void backpropogate(State* s, int winner);

#endif // __MCTS_H__
