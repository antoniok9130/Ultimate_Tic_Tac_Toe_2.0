#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>

#include <MCTS.h>
#include <UTTT.h>
#include <capi.h>

using namespace std;

int main(){
    MCTS m;
    cout << m.getCurrentPlayer() << " == " << P2 << endl;
    // MCTS::runParallelIterations(&m, 2000000);
    m.chooseMove(4, 4);
    cout << m.getCurrentPlayer() << " == " << P1 << endl;
    cout << m << endl;
    m.chooseMove(4, 6);
    cout << m << endl;
    cout << m.getPlayerAt(4, 4) << endl;
}
