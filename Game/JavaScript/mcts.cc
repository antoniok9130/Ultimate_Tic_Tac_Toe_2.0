
#include "mcts.h"
#include <ctime>
#include <cmath>
#include <iostream>
#include <bitset>

using namespace std; 

int mcts_seed = time(NULL);
inline int fastrand() {
    mcts_seed = (214013 * mcts_seed + 2531011);
    return (mcts_seed >> 16) & 0x7FFF;
}

// constexpr unsigned int twoInRow[9][4] = {
//     {0b011000000, 0b000100100, 0b000010001, 0},
//     {0b101000000, 0b000010010, 0, 0},
//     {0b110000000, 0b000001001, 0b000010100, 0},
//     {0b100000100, 0b000011000, 0, 0},
//     {0b100000001, 0b010000010, 0b001000100, 0b000101000},
//     {0b001000001, 0b000110000, 0, 0},
//     {0b000000011, 0b001010000, 0b100100000, 0},
//     {0b010010000, 0b000000101, 0, 0},
//     {0b000000110, 0b100010000, 0b001001000, 0}
// };

// bool check2InRow(const int& quadrant, const int& position){
//     const unsigned int* conditions = twoInRow[position];
//     for (int i = 0; i<4 && conditions[i] != 0; ++i){
//         if ((quadrant & conditions[i]) == conditions[i]){
//             return true;
//         }
//     }
//     return false;
// }
bool check2InRow(const int& position, const unsigned int& quadrant){
#ifdef REVERSE_BOARD
    switch(position){
        case 0:
            return ((quadrant & 0b011000000) == 0b011000000) ||
                   ((quadrant & 0b000100100) == 0b000100100) ||
                   ((quadrant & 0b000010001) == 0b000010001);
        case 1:
            return (((quadrant & 0b101000000) == 0b101000000) ||
                    ((quadrant & 0b000010010) == 0b000010010));
        case 2:
            return ((quadrant & 0b110000000) == 0b110000000) ||
                   ((quadrant & 0b000001001) == 0b000001001) ||
                   ((quadrant & 0b000010100) == 0b000010100);
        case 3:
            return ((quadrant & 0b100000100) == 0b100000100) ||
                   ((quadrant & 0b000011000) == 0b000011000);
        case 4:
            return ((quadrant & 0b100000001) == 0b100000001) ||
                   ((quadrant & 0b010000010) == 0b010000010) ||
                   ((quadrant & 0b001000100) == 0b001000100) ||
                   ((quadrant & 0b000101000) == 0b000101000);
        case 5:
            return ((quadrant & 0b001000001) == 0b001000001) ||
                   ((quadrant & 0b000110000) == 0b000110000);
        case 6:
            return ((quadrant & 0b000000011) == 0b000000011) ||
                   ((quadrant & 0b001010000) == 0b001010000) ||
                   ((quadrant & 0b100100000) == 0b100100000);
        case 7:
            return ((quadrant & 0b010010000) == 0b010010000) ||
                   ((quadrant & 0b000000101) == 0b000000101);
        case 8:
            return ((quadrant & 0b000000110) == 0b000000110) ||
                   ((quadrant & 0b100010000) == 0b100010000) ||
                   ((quadrant & 0b001001000) == 0b001001000);
        default:
            return false;
    }
#else
    switch(position){
        case 0:
            return ((quadrant & 0b000000110) == 0b000000110) ||
                   ((quadrant & 0b001001000) == 0b001001000) ||
                   ((quadrant & 0b100010000) == 0b100010000);
        case 1:
            return (((quadrant & 0b000000101) == 0b000000101) ||
                    ((quadrant & 0b010010000) == 0b010010000));
        case 2:
            return ((quadrant & 0b000000011) == 0b110000000) ||
                   ((quadrant & 0b100100000) == 0b100100000) ||
                   ((quadrant & 0b001010000) == 0b001010000);
        case 3:
            return ((quadrant & 0b001000001) == 0b001000001) ||
                   ((quadrant & 0b000110000) == 0b000110000);
        case 4:
            return ((quadrant & 0b100000001) == 0b100000001) ||
                   ((quadrant & 0b010000010) == 0b010000010) ||
                   ((quadrant & 0b001000100) == 0b001000100) ||
                   ((quadrant & 0b000101000) == 0b000101000);
        case 5:
            return ((quadrant & 0b100000100) == 0b100000100) ||
                   ((quadrant & 0b000011000) == 0b000011000);
        case 6:
            return ((quadrant & 0b110000000) == 0b110000000) ||
                   ((quadrant & 0b000010100) == 0b000010100) ||
                   ((quadrant & 0b000001001) == 0b000001001);
        case 7:
            return ((quadrant & 0b000010010) == 0b000010010) ||
                   ((quadrant & 0b101000000) == 0b101000000);
        case 8:
            return ((quadrant & 0b011000000) == 0b011000000) ||
                   ((quadrant & 0b000010001) == 0b000010001) ||
                   ((quadrant & 0b000100100) == 0b000100100);
        default:
            return false;
    }
#endif
}

// #define SHOW_PROGRESS

void getMCTSMove(State* s, int& global, int& local, const unsigned int& numIterations){
    if (isWin(s, global, local)) return;
    
#ifdef SHOW_PROGRESS
    int length = 50;
    int step = numIterations/length;
#endif
    for (unsigned int i = 0; i<numIterations; ++i){
#ifdef CHECK_DEPTH
        select(s, 0);
#else
        select(s);
#endif
#ifdef SHOW_PROGRESS
        if (i%step == 0){
            cout << "\r[";
            for (int j = 0; j<(i/step); ++j){
                cout << "#";
            }
            for (int j = (i/step); j<length; ++j){
                cout << " ";
            }
            cout << "] | " << (i/step*100/length) << "%       ";
        }
        cout.flush();
#endif
    }
#ifdef SHOW_PROGRESS
    cout << "\r                                              " << endl;
#endif
    
    if (s->getNumVisits() == 0){
        throw "No Move Found...";
    }
    // Get Most Visited Child
    State* child = s->getChildren();
    State* mostVisitedChild = nullptr;
    for (int i = 0; i < s->getNumChildren(); ++i){
        if (mostVisitedChild == nullptr ||
            child->getNumVisits() > mostVisitedChild->getNumVisits() || 
            (child->getNumVisits() == mostVisitedChild->getNumVisits() && (fastrand() % 2 == 1))){
            mostVisitedChild = child;
        }
#ifdef SHOW_PROGRESS
        cout << child->getGlobal() << " " << child->getLocal() << ":  " << child->getNumVisits() << endl;
#endif
        ++child;
    }
    global = mostVisitedChild->getGlobal();
    local = mostVisitedChild->getLocal();
#ifndef GENERATE_MODE
   cout << "w: " << mostVisitedChild->getNumWins() << "  v: " << mostVisitedChild->getNumVisits() << endl;
   cout << "Confidence:  " << (double(mostVisitedChild->getNumWins())/mostVisitedChild->getNumVisits()) << endl;
#endif
//     child = s->getChildren();
//     cout << child << " " << s->getNumChildren() << endl;
//     State* onlyChild = new State{mostVisitedChild};
//     cout << onlyChild << " " << onlyChild->getParent() << endl;
//     cout << s << endl;
//     mostVisitedChild->setChildren(nullptr);
//     delete[] child;
//     s->setChildren(onlyChild);
//     s->getNumChildren() = -1;
//     cout << s->getChildren() << endl;
}

bool isWin(State* s, int& global, int& local){
    unsigned int board = s->getBoard(0) | s->getBoard(1);
    unsigned int boardP, quadrant, quadrantP;
    if (IS_FILLED(board, local)){ // Next Quadrant is already filled
        boardP = s->getBoard();
        for (int i = 0; i<9; ++i){
            if (IS_EMPTY(board, i) && check2InRow(i, boardP)){
                quadrant = s->getQuadrant(i, 0) | s->getQuadrant(i, 1);
                quadrantP = s->getQuadrant(i);
                for (int j = 0; j<9; ++j){
                    if (IS_EMPTY(quadrant, j) && check2InRow(j, quadrantP)){
                        global = i;
                        local = j;
                        return true;
                    }
                }
            }
        }
    }
    else if (check2InRow(board, local)){
        quadrant = s->getQuadrant(local, 0) | s->getQuadrant(local, 1);
        quadrantP = s->getQuadrant(local);
        for (int i = 0; i<9; ++i){
            if (IS_EMPTY(quadrant, i) && check2InRow(i, quadrantP)){
                global = local;
                local = i;
                return true;
            }
        }
    }
    return false;
}

#ifdef CHECK_DEPTH
void select(State* s, int depth){
    if (depth > 81){
        throw "Select depth too deep";
    }
#else
void select(State* s){
#endif
    if (s->getNumChildren() == 0){
        if (s->getWinner() != N){
            backpropogate(s, s->getWinner());
        }
        else if (!s->empty() && s->getNumVisits() == 0){
            backpropogate(s, simulate(s));
        }
        else{
#ifdef CHECK_DEPTH
            expand(s, depth+1);
#else
            expand(s);
#endif
        }
    }
    else{
        // Get Child with Max UCT
#ifndef STORE_UCT
        double s2lnpv = sqrt(2*log(s->getNumVisits()));
#endif
        State* child = s->getChildren();
        State* maxUCTchild = nullptr;
        double maxUCT = 0, UCT = 0;
#ifdef CHECK_DEPTH
        if (s->getNumChildren() < 0 || s->getNumChildren() > 81){
            throw "Invalid Number of Children";
        }
#endif
        for (int i = 0; i<s->getNumChildren(); ++i){
#ifndef STORE_UCT
            unsigned long v = child->getNumVisits();
            UCT = v == 0 ? 100 : (child->getNumWins()+sqrt(v)*s2lnpv)/v;
#else
            UCT = child->getUCT();
#endif
            if (UCT > maxUCT){
                maxUCT = UCT;
                maxUCTchild = child;
            }
            ++child;
        }
#ifdef CHECK_DEPTH
        select(maxUCTchild, depth+1);
#else
        select(maxUCTchild);
#endif
    }
}

#ifdef CHECK_DEPTH
void checkpoint(){
    cout << "here" << endl;
}
    
void expand(State* s, int depth){
    if (depth > 81){
        cout << *s << endl;
        throw "Expand depth too deep";
    }
#else
void expand(State* s){
#endif
    if (s->getNumChildren() == 0){
        unsigned int board = s->getBoard(0) | s->getBoard(1);
        const unsigned int l = s->getLocal();
        if (!s->empty() && IS_EMPTY(board, l)){
            unsigned int moves = (s->getQuadrant(l, 0) | s->getQuadrant(l, 1)) & 0x1ff;
            s->getNumChildren() = 9-__builtin_popcountll(moves);
            State* child = new State[s->getNumChildren()];
            s->setChildren(child);
            for (unsigned int i = 0; i<9; ++i){
                if (IS_EMPTY(moves, i)){
#ifdef CHECK_DEPTH
                    child->init(s, l, i);
                    if (child->empty() || child->getWinner() != N){
                        checkpoint();
                    }
                    child++;
#else
                    (child++)->init(s, l, i);
#endif
                }
            }
        }
        else{
            unsigned int moves[9];
            for (unsigned int i = 0; i<9; ++i){
                if (IS_EMPTY(board, i)){
                    moves[i] = (s->getQuadrant(i, 0) | s->getQuadrant(i, 1)) & 0x1ff;
                    s->getNumChildren() += 9-__builtin_popcountll(moves[i]);
                }
                else{
                    moves[i] = 1000; // Invalid
                }
            }
            State* child = new State[s->getNumChildren()];
            s->setChildren(child);
            for (unsigned int i = 0; i<9; ++i){
                if (moves[i] != 1000){
                    for (unsigned int j = 0; j<9; ++j){
                        if (IS_EMPTY(moves[i], j)){
#ifdef CHECK_DEPTH
                            child->init(s, i, j);
                            if (child->empty() || child->getWinner() != N){
                                checkpoint();
                            }
                            child++;
#else
                            (child++)->init(s, i, j);
#endif
                        }
                    }
                }
            }
        }
        
        if (s->getNumChildren() > 0){
            State* randomChild = s->getChildren()+(fastrand() % s->getNumChildren());
            backpropogate(randomChild, simulate(randomChild));
        }
    }
}
    
#define CHECK_SIMULATE_FOR_WIN

int simulate(State* s){
    if (s->getWinner() != N){
        return s->getWinner();
    }
    unsigned long long boards[3] = {s->getBoard(0), s->getBoard(1), 0};
    boards[2] = boards[0] | boards[1];
    unsigned long long quadrants[3][9];
    for (int i = 0; i<9; ++i){
        quadrants[0][i] = s->getQuadrant(i, 0);
        quadrants[1][i] = s->getQuadrant(i, 1);
        quadrants[2][i] = quadrants[0][i] | quadrants[1][i];
    }
    unsigned int global = s->getGlobal();
    unsigned int local = s->getLocal();
    bool player = (bool) s->getCurrentPlayer();
    unsigned long long board;
#ifdef CHECK_DEPTH
    int length = 0;
#endif
    while(true){
        player = !player;
        if (IS_EMPTY(boards[2], local)){
            global = local;
#ifdef CHECK_SIMULATE_FOR_WIN
            board = boards[player] & ~boards[!player];
            if (check2InRow(global, board)){
                for (local = 0; local<9; ++local){
                    if (check2InRow(local, quadrants[player][global])){
                        return player ? P2 : P1;
                    }
                }
            }
#endif
        }
        else{
#ifdef CHECK_SIMULATE_FOR_WIN
            board = boards[player] & ~boards[!player];
            for (global = 0; global<9; ++global){
                if (check2InRow(global, board)){
                    for (local = 0; local<9; ++local){
                        if (check2InRow(local, quadrants[player][global])){
                            return player ? P2 : P1;
                        }
                    }
                }
            }
#endif
#ifdef CHECK_DEPTH
            int stuck = 0;
#endif
            do {
                global = fastrand() % 9;
#ifdef CHECK_DEPTH
                if ((++stuck) > 1000){
                    cout << bitset<9>(boards[2]) << endl;
                    throw "Spinning trying to find global in simulation";
                }
#endif
            } while (IS_FILLED(boards[2], global));
        }
        
#ifdef CHECK_DEPTH
        int stuck = 0;
#endif
        do {
            local = fastrand() % 9;
#ifdef CHECK_DEPTH
            if ((++stuck) > 1000){
                cout << bitset<9>(quadrants[2][global]) << endl;
                throw "Spinning trying to find local in simulation";
            }
#endif
        } while (IS_FILLED(quadrants[2][global], local));
                 
#ifdef REVERSE_BOARD
        quadrants[player][global] |= (1ull << (8-local));
        quadrants[2][global] |= (1ull << (8-local));
#else
        quadrants[player][global] |= (1ull << local);
        quadrants[2][global] |= (1ull << local);
#endif
        if (check3InRow(local, quadrants[player][global])){
            boards[player] |= (1ull << global);
            boards[2] = boards[0] | boards[1];
            if (IS_TIE(boards[2])){
                return T;
            }
#ifndef CHECK_SIMULATE_FOR_WIN
            else if (check3InRow(global, boards[player] & ~boards[!player])){
                return player ? P2 : P1;
            }
#endif
        }
        else if (IS_TIE(quadrants[2][global])){
            boards[0] |= (1ull << global);
            boards[1] |= (1ull << global);
            boards[2] = boards[0] | boards[1];
            if (IS_TIE(boards[2])){
                return T;
            }
        }
#ifdef CHECK_DEPTH
        ++length;
        if (length > 81){
            cout << &sim << endl;
            cout << sim.getCurrentPlayer() << endl;
            cout << sim.getWinner() << endl;
            cout << global << " " << local << endl;
            throw "Invalid Simulation";
        }
#endif
    }
}


void backpropogate(State* s, int winner){
    if (winner == P1){
        winner = 0;
    }
    else if (winner == P2){
        winner = 1;
    }
    else {
        winner = -1;
    }
    State* current = s;
#ifdef CHECK_DEPTH
    int length = 0;
#endif
    while (current != nullptr){
        if (current->getCurrentPlayer() == winner){
            ++(current->getNumWins());
        }
        ++(current->getNumVisits());
#ifdef STORE_UCT
        current->setUCTbit();
#endif
        current = current->getParent();
#ifdef CHECK_DEPTH
        ++length;
        if (current == s){
            cout << length << endl;
            throw "Backpropogation entered loop";
        }
        if (length > 75){
            cout << current << endl;
            if (length > 81){
                throw "Invalid BackPropogation";
            }
        }
#endif
    }
}
