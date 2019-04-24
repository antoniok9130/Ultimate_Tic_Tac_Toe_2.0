#include <iostream>
#include <ctime>
#include <bitset>
#include "state.h"
#include "mcts.h"

using namespace std;

int main_seed = time(NULL);
inline int fastrand() {
    main_seed = (214013 * main_seed + 2531011);
    return (main_seed >> 16) & 0x7FFF;
}

void getRandomMove(State* state, int& global, int& local){
    unsigned int board = state->getBoard(0) | state->getBoard(1);
    global = local != -1 ? local : fastrand() % 9;
    while (IS_FILLED(board, global)){
        global = fastrand() % 9;
    }
    
    unsigned int quadrant = state->getQuadrant(global, 0) | state->getQuadrant(global, 1);
    do {
        local = fastrand() % 9;
    } while (IS_FILLED(quadrant, local));
}


void playGame(void (*getP1Move)(State*, int&, int&),
              void (*getP2Move)(State*, int&, int&)){
    State s;
    int global = -1, local = -1;
    
    while (s.getWinner() == N){
        getP1Move(&s, global, local);
        s.setMove(global, local);
        s.switchPlayer();
        
        if (s.getWinner() != N){
            break;
        }

        getP2Move(&s, global, local);
        s.setMove(global, local);
        s.switchPlayer();
    }
    
//     cout << s.getWinner() << endl;
//     cout << &s << endl << endl;
}

int main(){
    try{
//         srand(time(NULL));
//         int n = 2000000;
        
//         clock_t start = clock();
//         numTrue = 0;
//         for (int i = 0; i<n; ++i){
//             playGame(&getRandomMove, &getRandomMove);
//         }
//         clock_t end = clock();
//         cout << numTrue << endl;
//         cout << "Took " << (double(end-start)/CLOCKS_PER_SEC) << " to run " << n << " simulations" << endl;
        
        cout << sizeof(State) << endl;
        
    } catch(const char* error1){
        cerr << error1 << endl;
        return 1;
    }
    return 0;
}
