#include <cstring>
#include <sstream>

#include "../capi.h"

using namespace std;

extern "C" {
    const int UTTT_N(){ return N; }
    const int UTTT_P1(){ return P1; }
    const int UTTT_P2(){ return P2; }
    const int UTTT_T(){ return T; }

    UTTT* new_UTTT(){ return new UTTT(); }
    void delete_UTTT(UTTT* u){ delete u; }

    int UTTT_empty(UTTT* u){ return u->empty(); }

    int UTTT_getCurrentPlayer(UTTT* u){ return u->getCurrentPlayer(); }
    void UTTT_setCurrentPlayer(UTTT* u, int player){ return u->setCurrentPlayer((bool) player); }
    void UTTT_switchPlayer(UTTT* u){ u->switchPlayer(); }

    int UTTT_getWinner(UTTT* u){ return u->getWinner(); }

    unsigned int UTTT_getQuadrant(UTTT* u, const unsigned int quadrant){
        return u->getQuadrant(quadrant);
    }
    unsigned int UTTT_getQuadrantForPlayer(UTTT* u, const unsigned int quadrant, const int player){
        return u->getQuadrant(quadrant, player);
    }

    int UTTT_getPlayerAt(UTTT* u, const unsigned int quadrant){
        return u->getPlayerAt(quadrant);
    }
    int UTTT_getPlayerAtQuadrant(UTTT* u, const unsigned int quadrant, const unsigned int local){
        return u->getPlayerAt(quadrant, local);
    }

    int UTTT_setMove(UTTT* u, const unsigned long long quadrant, const unsigned long long local){
        return u->setMove(quadrant, local);
    }
    int UTTT_updateBoard(UTTT* u, const unsigned long long quadrant, const unsigned long long local){
        return u->updateBoard(quadrant, local);
    }

    unsigned int UTTT_getBoard(UTTT* u){
        return u->getBoard();
    }
    unsigned int UTTT_getBoardForPlayer(UTTT* u, const int player){
        return u->getBoard(player);
    }
    unsigned int UTTT_getLocal(UTTT* u){
        return u->getLocal();
    }
    unsigned int UTTT_getGlobal(UTTT* u){
        return u->getGlobal();
    }

    int UTTT_check3InRow(const unsigned int quadrant, const unsigned int local){
        return UTTT::check3InRow(quadrant, local);
    }
    char* UTTT_printBoard(UTTT* u){
        ostringstream out;
        out << *u;
        string s = out.str();
        char* board = (char*) malloc((s.size() + 1)*sizeof(char));
        strcpy(board, s.c_str());
        return board;
    }


    /*********************************************************************************************/

    MCTS* new_MCTS(){ return new MCTS(); }
    void delete_MCTS(MCTS* m){ delete m; }

    MCTS* MCTS_getParent(MCTS* m){ return m->getParent(); }
    void MCTS_setParent(MCTS* m, MCTS* parent){ m->setParent(parent); }

    int MCTS_getNumChildren(MCTS* m){ return m->getNumChildren(); }

    void MCTS_makeMove(MCTS* m){ m->makeMove(); }

    unsigned long MCTS_getNumWins(MCTS* m){ return m->getNumWins(); }
    unsigned long MCTS_getNumVisits(MCTS* m){ return m->getNumVisits(); }
    void MCTS_incrementWins(MCTS* m, int amount){ m->incrementWins(amount); }
    void MCTS_incrementVisits(MCTS* m, int amount){ m->incrementVisits(amount); }

    MCTS* MCTS_select(MCTS* m){ return MCTS::select(m); }
    MCTS* MCTS_expand(MCTS* m){ return MCTS::expand(m); }
    int MCTS_simulate(MCTS* m){ return MCTS::simulate(m); }
    void MCTS_backprop(MCTS* m, int winner){ MCTS::backprop(m, winner); }

    MCTS* MCTS_select_expand(MCTS* m){ return MCTS::select_expand(m); }
    void MCTS_runIterations(MCTS* m, int numIterations){ return MCTS::runIterations(m, numIterations); }
    void MCTS_runParallelIterations(MCTS* m, int numIterations){ return MCTS::runParallelIterations(m, numIterations); }
}
