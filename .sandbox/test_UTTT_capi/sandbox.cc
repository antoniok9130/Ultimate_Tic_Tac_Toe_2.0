#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>

#include <MCTS.h>
#include <capi.h>

using namespace std;

int main(){
    MCTS m;
    char* board = UTTT_printBoard(&m);
    cout << (const char*) board << endl;
    free(board);

    MCTS* s = MCTS::select(&m);
    MCTS* e = MCTS::expand(s);
    int winner = MCTS::simulate(e);
    MCTS::backprop(e, winner);
}
