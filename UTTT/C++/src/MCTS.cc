#include <bitset>
#include <cmath>
#include <ctime>
#include <iostream>

using namespace std;

#include "../MCTS.h"

MCTS::MCTS(){

}

    /*
    operator=
    w {other->w},
    v {other->v},
    #ifdef STORE_UCT
    UCT {other->UCT},
    #endif
    UCT = other.UCT;
    #endif
    */
MCTS::MCTS(const MCTS& other):
    UTTT(other),
    parent {other.parent},
    children {other.children},
    numChildren {other.numChildren},
    w {other.w},
    v {other.v}
    #ifdef STORE_UCT
    , UCT {other->UCT}
    #endif
    {}
MCTS::MCTS(MCTS* parent, const unsigned int global, const unsigned int local):
    UTTT(*parent),
    parent {parent} {
    setCurrentPlayer(1-parent->getCurrentPlayer());
    setMove(global, local);
}


// UTTT& UTTT::operator=(const UTTT& other){
//     children = other.children;
//     numChildren = other.numChildren;

//     parent = other.parent;
//     n1 = other.n1;
//     n2 = other.n2;
//     n3 = other.n3;

//     return *this;
// }


void MCTS::init(MCTS* parent, const unsigned int global,
                              const unsigned int local){
    this->parent = parent;
    n1 = parent->n1;
    n2 = parent->n2;
    n3 = parent->n3;
    setCurrentPlayer(1-parent->getCurrentPlayer());
    setMove(global, local);
}

MCTS* MCTS::getParent(){ return parent; }
void MCTS::setParent(MCTS* parent){ this->parent = parent; }

int MCTS::getNumChildren(){ return numChildren; }
shared_ptr<MCTS[]> MCTS::getChildren(){ return children; }
void MCTS::allocateChildren(int numChildren){
    this->numChildren = numChildren;
    children = std::shared_ptr<MCTS[]>(new MCTS[numChildren]);
}

bool MCTS::setMove(const unsigned long long global,
                   const unsigned long long local){
    if (numChildren > 0){
        for (int i = 0; i<numChildren; ++i){
            if (children[i].getGlobal() == global &&
                children[i].getLocal() == local){
                *this = children[i];
                parent = nullptr;
                for (i = 0; i<numChildren; ++i){
                    children[i].parent = this;
                }
                return false;
            }
        }
    }
    return UTTT::setMove(global, local);
}

unsigned long MCTS::getNumWins(){
    return w;
}
unsigned long MCTS::getNumVisits(){
    return v;
}
void MCTS::incrementWins(){ ++w; }
void MCTS::incrementVisits(){ ++v; }

#ifdef STORE_UCT
void UTTT::setUCTbit(){
    n3 |= (1ull << 63); // 0x8000000000000000; //
}
double& UTTT::getUCT(){
    if (n3 >> 63){
        UCT = v == 0 ? 100 : (parent ? (w+sqrt(2*v*log(parent->v)))/v : double(w)/v);
        n3 &= ~(1ull << 63); // 0x7fffffffffffffff; //
    }
    return UCT;
}
#endif


int mcts_seed = time(NULL);
inline int fastrand() {
    mcts_seed = (214013 * mcts_seed + 2531011);
    return (mcts_seed >> 16) & 0x7FFF;
}

bool check2InRow(const int& position, const unsigned int& quadrant){
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
}

MCTS* MCTS::select(MCTS* m){
    if (m->getWinner() == N){
        while (m->getNumChildren() > 0){
            // Get Child with Max UCT
#ifndef STORE_UCT
            double s2lnpv = sqrt(2*log(m->getNumVisits()));
#endif
            MCTS* child = m->getChildren().get();
            const int numChildren = m->getNumChildren();
            double maxUCT = 0, UCT = 0;
            for (int i = 0; i < numChildren; ++i){
#ifndef STORE_UCT
                unsigned long v = child->getNumVisits();
                UCT = v == 0 ? fastrand() : (child->getNumWins()+sqrt(v)*s2lnpv)/v;
#else
                UCT = child->getUCT();
#endif
                if (UCT > maxUCT){
                    maxUCT = UCT;
                    m = child;
                }
                ++child;
            }
        }
    }
    return m;
}

MCTS* MCTS::expand(MCTS* m){
    if (m->getNumChildren() == 0){
        if (m->getWinner() != N || (!m->empty() && m->getNumVisits() == 0)){
            return m;
        }

        unsigned int board = m->getBoard(0) | m->getBoard(1);
        const unsigned int l = m->getLocal();
        if (!m->empty() && IS_EMPTY(board, l)){
            unsigned int moves = (m->getQuadrant(l, 0) | m->getQuadrant(l, 1)) & 0x1ff;
            m->allocateChildren(9-__builtin_popcountll(moves));
            MCTS* child = m->getChildren().get();
            for (unsigned int i = 0; i<9; ++i){
                if (IS_EMPTY(moves, i)){
                    (child++)->init(m, l, i);
                }
            }
        }
        else{
            unsigned int moves[9];
            int numChildren = 0;
            for (unsigned int i = 0; i<9; ++i){
                if (IS_EMPTY(board, i)){
                    moves[i] = (m->getQuadrant(i, 0) | m->getQuadrant(i, 1)) & 0x1ff;
                    numChildren += 9 - __builtin_popcountll(moves[i]);
                }
                else{
                    moves[i] = 1000; // Invalid
                }
            }
            m->allocateChildren(numChildren);
            MCTS* child = m->getChildren().get();
            for (unsigned int i = 0; i<9; ++i){
                if (moves[i] != 1000){
                    for (unsigned int j = 0; j<9; ++j){
                        if (IS_EMPTY(moves[i], j)){
                            (child++)->init(m, i, j);
                        }
                    }
                }
            }
        }

        if (m->getNumChildren() > 0){
            return m->getChildren().get()+(fastrand() % m->getNumChildren());
        }
    }
    return m;
}

#define CHECK_SIMULATE_FOR_WIN

int MCTS::simulate(MCTS* m){
    if (m->getWinner() != N){
        return m->getWinner();
    }
    unsigned long long boards[3] = {m->getBoard(0), m->getBoard(1), 0};
    boards[2] = boards[0] | boards[1];
    unsigned long long quadrants[3][9];
    for (int i = 0; i<9; ++i){
        quadrants[0][i] = m->getQuadrant(i, 0);
        quadrants[1][i] = m->getQuadrant(i, 1);
        quadrants[2][i] = quadrants[0][i] | quadrants[1][i];
    }
    unsigned int global = m->getGlobal();
    unsigned int local = m->getLocal();
    bool player = (bool) m->getCurrentPlayer();
    unsigned long long board;
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
            do {
                global = fastrand() % 9;
            } while (IS_FILLED(boards[2], global));
        }

        do {
            local = fastrand() % 9;
        } while (IS_FILLED(quadrants[2][global], local));

        quadrants[player][global] |= (1ull << local);
        quadrants[2][global] |= (1ull << local);
        if (UTTT::check3InRow(quadrants[player][global], local)){
            boards[player] |= (1ull << global);
            boards[2] = boards[0] | boards[1];
            if (IS_TIE(boards[2])){
                return T;
            }
#ifndef CHECK_SIMULATE_FOR_WIN
            else if (check3InRow(boards[player] & ~boards[!player], global)){
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
    }
}


void MCTS::backprop(MCTS* m, int winner){
    if (winner == P1){
        winner = 0;
    }
    else if (winner == P2){
        winner = 1;
    }
    else {
        winner = -1;
    }
    MCTS* current = m;
    while (current != nullptr){
        if (current->getCurrentPlayer() == winner){
            current->incrementWins();
        }
        current->incrementVisits();
#ifdef STORE_UCT
        current->setUCTbit();
#endif
        current = current->getParent();
    }
}
