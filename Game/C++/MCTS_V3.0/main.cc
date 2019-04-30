#include <iostream>
#include <ctime>
#include <bitset>
#include <string>
#include <sstream>
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
    state->switchPlayer();
}

void getHumanMove(State* state, int& global, int& local){
    unsigned int board = state->getBoard(0) | state->getBoard(1);
//     cout << *state << endl;
    string s;
    int g, l;
    while (true){
        cout << "Enter Move:  ";
        if (!getline(cin, s)){
            throw "Error while getting line from stdin";
        }
        istringstream iss {s};
        if (!(iss >> g)){
            throw "Error while reading global from stdin";
        }
        if (!(iss >> l)){
            l = g;
            g = local;
        }
        if (g < 0 || g > 8 || IS_FILLED(board, g) || 
            (local != -1 && g != local)){
            cout << "Invalid global input:  " << g << endl;
            cout << "Current Global:  " << local << endl << endl;
            continue;
        }
        unsigned int quadrant = state->getQuadrant(g, 0) | state->getQuadrant(g, 1);
        if (l < 0 || l > 8 || IS_FILLED(quadrant, l)){
            cout << "Invalid local input:  " << l << endl;
            continue;
        }
        cout << "Entered Move:  " << g << " " << l << endl;
        global = g;
        local = l;
        return;
    }
}

void getMCTSMove(State* state, int& global, int& local){
    clock_t start = clock();
    getMCTSMove(state, global, local, 2000000);
    clock_t end = clock();
    cout << "Took " << double(end-start)/CLOCKS_PER_SEC << " seconds to compute move" << endl;
}


void playGame(void (*getP1Move)(State*, int&, int&),
              void (*getP2Move)(State*, int&, int&)){
    State s;
    int global = 4, local = 4;
    s.setMove(global, local);
    
    cout << s << endl;
    
    while (s.getWinner() == N){
        getP1Move(&s, global, local);
        s.setMove(global, local);
        cout << s << endl;
        
        if (s.getWinner() != N){
            break;
        }

        getP2Move(&s, global, local);
        s.setMove(global, local);
        cout << s << endl;
    }
    
    cout << s.getWinner() << endl;
    cout << &s << endl << endl;
}

int main(){
#ifndef CHECK_DEPTH
    try{
#endif
        playGame(&getMCTSMove, &getMCTSMove);
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
        
//         cout << sizeof(State) << endl;
      
#ifndef CHECK_DEPTH  
    } catch(const char* error1){
        cerr << error1 << endl;
        return 1;
    }
    return 0;
#endif
}
