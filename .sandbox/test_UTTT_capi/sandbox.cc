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
    while (m.getWinner() == N){
        MCTS::runIterations(&m, 10000);
        m.makeMove();
    }
    cout << m << endl << endl;
    cout << m.getWinner() << endl;
}
