
#include "mcts.h"
#include <ctime>

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
bool check2InRow(const unsigned int& quadrant, const int& position){
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
}

void getMCTSMove(State* s, int& global, int& local, const unsigned int& numIterations){
    if (isWin(s, global, local)) return;
    
    for (unsigned int i = 0; i<numIterations; ++i){
        select(s);
    }
    
    if (s->getNumVisits() == 0){
        throw "No Move Found...";
    }
    getChildVisitedMost(s, global, local);
}

bool isWin(State* s, int& global, int& local){
    unsigned int board = s->getBoard(0) | s->getBoard(1);
    unsigned int boardP, quadrant, quadrantP;
    if (IS_FILLED(board, local)){ // Next Quadrant is already filled
        boardP = s->getBoard();
        for (int i = 0; i<9; ++i){
            if (IS_EMPTY(board, i) && check2InRow(boardP, i)){
                quadrant = s->getQuadrant(i, 0) | s->getQuadrant(i, 1);
                quadrantP = s->getQuadrant(i);
                for (int j = 0; j<9; ++j){
                    if (IS_EMPTY(quadrant, j) && check2InRow(quadrantP, j)){
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
            if (IS_EMPTY(quadrant, i) && check2InRow(quadrantP, i)){
                global = local;
                local = i;
                return true;
            }
        }
    }
    return false;
}

static void getChildVisitedMost(State *s, int& global, int& local){
    State* child = s->getChildren();
    State* mostVisitedChild = nullptr;
    for (int i = 0; i < s->getNumChildren(); ++i){
        if (mostVisitedChild == nullptr ||
            children->getNumVisits() > mostVisitedChild->getNumVisits() || 
            (child->getNumVisits() == mostVisitedChild->getNumVisits() && (fastrand() % 2 == 1))){
            mostVisitedChild = child;
        }
        ++child;
    }
    global = mostVisitedChild->getGlobal();
    local = mostVisitedChild->getLocal();
}

void select(State* s){
    if (s->getNumChildren() == 0){
        if (s->getWinner() != N){
            backpropogate(node, node->getWinner());
        }
        else if (s->getNumVisits() == 0){
            int winner = simulate(s);
            backpropogate(node, winner);
        }
        else{
            expand(s);
        }
    }
    else{
        // Get Child with Max UCT
        double s2lnpv = sqrt(2*log(s->getNumVisits()));
        State* child = s->getChildren();
        State* maxUCTchild = nullptr;
        double maxUCT = 0;
        for (int i = 0; i<s->getNumChildren(); ++i){
            double UCT = child->getNumVisits() == 0 ? 100 : (child->getNumWins()+sqrt(child->getNumVisits())*s2lnpv)/child->getNumVisits();
            if (UCT > maxUCT){
                maxUCT = UCT;
                maxUCTchild = child;
            }
            ++child;
        }
        select(maxUCTchild);
    }
}

void expand(State* s){
    if (s->getNumChildren() == 0){
        unsigned int board = s->getBoard(0) | s->getBoard(1);
    }
}
