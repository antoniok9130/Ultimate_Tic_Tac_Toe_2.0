#include <iostream>
#include <ctime>
#include <bitset>
#include <string>
#include <sstream>
#include <fstream>
#include "state.h"
#include "mcts.h"

using namespace std;

#define ITERATIONS 2000000

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


void getAIMove(State* state, int& global, int& local){
#ifndef GENERATE_MODE
    clock_t start = clock();
#endif
    getMCTSMove(state, global, local, ITERATIONS);
#ifndef GENERATE_MODE
    clock_t end = clock();
    cout << "Move:  " << global << " " << local << endl;
    cout << "Took " << double(end-start)/CLOCKS_PER_SEC << " seconds to compute move" << endl;
#endif
}


void playGame(void (*getP1Move)(State*, int&, int&),
              void (*getP2Move)(State*, int&, int&)){
    State s;
    int global = 4, local = 4;
    //s.setMove(global, local);
    
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



void generateGame(ostream& out, int& global, int& local){
    try{
        State s;
        out << global << local;
        s.setMove(global, local);

        while (s.getWinner() == N){
            getAIMove(&s, global, local);
            out << global << local;
            s.setMove(global, local);
        }

        out << ":" << s.getWinner() << endl;
    } catch (...){
        cerr << "Error Completing Game" << endl;
    }
}
constexpr int numMovePriorities = 172;
const int movePriorities[numMovePriorities][2] = {
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 0}, {4, 0}, {4, 2}, {4, 2}, {4, 6}, {4, 6}, {4, 8}, {4, 8}, 
    {0, 0}, {0, 2}, {0, 6}, {0, 8}, {2, 0}, {2, 2}, {2, 6}, {2, 8}, {6, 0}, {6, 2}, {6, 6}, {6, 8}, {8, 0}, {8, 2}, {8, 6}, {8, 8}, 
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 0}, {4, 0}, {4, 2}, {4, 2}, {4, 6}, {4, 6}, {4, 8}, {4, 8}, 
    {0, 0}, {0, 2}, {0, 6}, {0, 8}, {2, 0}, {2, 2}, {2, 6}, {2, 8}, {6, 0}, {6, 2}, {6, 6}, {6, 8}, {8, 0}, {8, 2}, {8, 6}, {8, 8}, 
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 0}, {4, 0}, {4, 2}, {4, 2}, {4, 6}, {4, 6}, {4, 8}, {4, 8}, 
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, 
    {4, 1}, {4, 3}, {4, 5}, {4, 7}, {1, 1}, {3, 3}, {5, 5}, {7, 7}, 
    {0, 1}, {0, 3}, {0, 5}, {0, 7}, {1, 0}, {1, 2}, {1, 3}, {1, 5}, {1, 6}, {1, 7}, {1, 8}, {2, 1}, {2, 3}, {2, 5}, {2, 7}, 
    {3, 0}, {3, 1}, {3, 2}, {3, 5}, {3, 6}, {3, 7}, {3, 8}, {5, 0}, {5, 1}, {5, 2}, {5, 3}, {5, 6}, {5, 7}, {5, 8}, 
    {6, 1}, {6, 3}, {6, 5}, {6, 7}, {7, 0}, {7, 1}, {7, 2}, {7, 3}, {7, 5}, {7, 6}, {7, 8}, 
    {8, 1}, {8, 3}, {8, 5}, {8, 7}, {0, 4}, {1, 4}, {2, 4}, {3, 4}, {5, 4}, {6, 4}, {7, 4}, {8, 4},
    {0, 0}, {0, 2}, {0, 6}, {0, 8}, {2, 0}, {2, 2}, {2, 6}, {2, 8}, {6, 0}, {6, 2}, {6, 6}, {6, 8}, {8, 0}, {8, 2}, {8, 6}, {8, 8}, 
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 0}, {4, 0}, {4, 2}, {4, 2}, {4, 6}, {4, 6}, {4, 8}, {4, 8}, 
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 4}
};

int main(int argc, char** argv){
#ifndef CHECK_DEPTH
    try{
#endif
#ifdef GENERATE_MODE
        int lognum = 0;
        long numIterations = 0;
        for (int i = 0; i < argc; ++i) {
            string arg{argv[i]};
            if (arg == "-l") {
                istringstream iss {argv[++i]};
                iss >> lognum;
            } else if (arg == "-i") {
                istringstream iss {argv[++i]};
                iss >> numIterations;
            }
        }
	cout << "Log Num:  " << lognum << endl;
	    cout << "Num Iterations:  " << ITERATIONS << endl;
        ostringstream logPath;
        logPath << "Games/games-l-" << lognum << "-i-" << numIterations << ".txt";
        
        std::ofstream logout;
        logout.open(logPath.str(), std::ios_base::app);
        int global, local;
        for (int i = 0; i<100000; ++i){
            global = movePriorities[i%numMovePriorities][0];
            local = movePriorities[i%numMovePriorities][1];
            generateGame(logout, global, local, numIterations);
        }
#else
        playGame(&getHumanMove, &getAIMove);
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
#endif
      
#ifndef CHECK_DEPTH  
    } catch(const char* error1){
        cerr << error1 << endl;
        return 1;
    }
    return 0;
#endif
}
