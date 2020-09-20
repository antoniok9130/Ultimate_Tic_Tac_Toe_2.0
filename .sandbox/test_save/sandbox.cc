#include <iostream>
#include <cstdlib>
#include <MCTS.h>

using namespace std;

typedef size_t (*func_t)(float*, int);

int main(){
    MCTS m;
    int length = -1;
    while ((++length) < 81 && m.getWinner() == N){
        m.makeMove();
        cout << m.getGlobal() << " " << m.getLocal() << endl;
    }
    cout << m << endl;
}
