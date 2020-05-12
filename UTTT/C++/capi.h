#pragma once

#include "MCTS.h"
#include "UTTT.h"

extern "C" {
    const int UTTT_N();
    const int UTTT_P1();
    const int UTTT_P2();
    const int UTTT_T();

    UTTT* new_UTTT();
    void delete_UTTT(UTTT*);

    int UTTT_empty(UTTT*);

    int UTTT_getCurrentPlayer(UTTT*);
    void UTTT_setCurrentPlayer(UTTT*, int player);
    void UTTT_switchPlayer(UTTT*);

    int UTTT_getWinner(UTTT*);

    unsigned int UTTT_getQuadrant(UTTT*, const unsigned int quadrant);
    unsigned int UTTT_getQuadrantForPlayer(UTTT*, const unsigned int quadrant, const int player);

    int UTTT_getPlayerAt(UTTT*, const unsigned int quadrant);
    int UTTT_getPlayerAtQuadrant(UTTT*, const unsigned int quadrant, const unsigned int local);

    int UTTT_isLegal(UTTT*, const unsigned int quadrant, const unsigned int local);

    int UTTT_setMove(UTTT*, const unsigned long long quadrant, const unsigned long long local);
    int UTTT_updateBoard(UTTT*, const unsigned long long quadrant, const unsigned long long local);

    unsigned int UTTT_getBoard(UTTT*);
    unsigned int UTTT_getBoardForPlayer(UTTT*, const int player);

    unsigned int UTTT_getLocal(UTTT*);
    unsigned int UTTT_getGlobal(UTTT*);

    int UTTT_check3InRow(const unsigned int quadrant, const unsigned int local);
    char* UTTT_printBoard(UTTT*);

    /*********************************************************************************************/

    MCTS* new_MCTS();
    void delete_MCTS(MCTS*);

    MCTS* MCTS_getParent(MCTS*);
    void MCTS_setParent(MCTS* m, MCTS* parent);

    int MCTS_getNumChildren(MCTS*);

    void MCTS_makeMove(MCTS* m);
    void MCTS_setMove(MCTS* m, const unsigned long long quadrant, const unsigned long long local);

    unsigned long MCTS_getNumWins(MCTS*);
    unsigned long MCTS_getNumVisits(MCTS*);
    void MCTS_incrementWins(MCTS*, int amount);
    void MCTS_incrementVisits(MCTS*, int amount);

    MCTS* MCTS_select(MCTS*);
    MCTS* MCTS_expand(MCTS*);
    int MCTS_simulate(MCTS*);
    void MCTS_backprop(MCTS*, int winner);

    MCTS* MCTS_select_expand(MCTS*);
    void MCTS_runIterations(MCTS*, int numIterations);
    void MCTS_runParallelIterations(MCTS*, int numIterations);

    /*********************************************************************************************/

    int MCTS_getHardcodedMove(const unsigned int quadrant, const unsigned int local);

}
