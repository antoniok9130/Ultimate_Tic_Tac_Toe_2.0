#include "state.h"
#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <vector>

#ifdef DEBUG
#include <bitset>
#endif

using namespace std;

#define F9 0x1ff // Gets first 9 bits

bool check3InRow(const unsigned int& local,
                 const unsigned int& quadrant){
    switch(local){
        case 0:
            return ((quadrant & 0b111000000) == 0b111000000) ||
                   ((quadrant & 0b100100100) == 0b100100100) ||
                   ((quadrant & 0b100010001) == 0b100010001);
        case 1:
            return ((quadrant & 0b111000000) == 0b111000000) ||
                   ((quadrant & 0b010010010) == 0b010010010);
        case 2:
            return ((quadrant & 0b111000000) == 0b111000000) ||
                   ((quadrant & 0b001001001) == 0b001001001) ||
                   ((quadrant & 0b001010100) == 0b001010100);
        case 3:
            return ((quadrant & 0b100100100) == 0b100100100) ||
                   ((quadrant & 0b000111000) == 0b000111000);
        case 4:
            return ((quadrant & 0b100010001) == 0b100010001) ||
                   ((quadrant & 0b010010010) == 0b010010010) ||
                   ((quadrant & 0b001010100) == 0b001010100) ||
                   ((quadrant & 0b000111000) == 0b000111000);
        case 5:
            return ((quadrant & 0b001001001) == 0b001001001) ||
                   ((quadrant & 0b000111000) == 0b000111000);
        case 6:
            return ((quadrant & 0b000000111) == 0b000000111) ||
                   ((quadrant & 0b001010100) == 0b001010100) ||
                   ((quadrant & 0b100100100) == 0b100100100);
        case 7:
            return ((quadrant & 0b010010010) == 0b010010010) ||
                   ((quadrant & 0b000000111) == 0b000000111);
        case 8:
            return ((quadrant & 0b000000111) == 0b000000111) ||
                   ((quadrant & 0b100010001) == 0b100010001) ||
                   ((quadrant & 0b001001001) == 0b001001001);
        default:
            return false;
    }
}

#ifdef __UTTT_HAS_MEMBERS__

State::State(){}
State::State(State* parent):
    parent {parent->parent},
    w {parent->w},
    n {parent->n},
    n1 {parent->n1},
    n2 {parent->n2},
    n3 {parent->n3}{}
State::State(State* parent, const unsigned int& global,
                             const unsigned int& local):
    parent {parent},
    w {parent->w},
    n {parent->n},
    n1 {parent->n1},
    n2 {parent->n2},
    n3 {parent->n3}{
    switchPlayer();
    setMove(global, local);
}
State::~State(){
    #ifdef __UTTT_STORES_CHILDREN__
    if (children){
//         for (int i = 0; i<numChildren; ++i){
//             delete child[i];
//         }
        delete[] children;
//         children = nullptr;
    }
    #endif
}
unsigned int& State::getNumChildren(){
     return numChildren;
}
State* State::getChildren(){
    return getChildren;
}
unsigned int& State::getNumWins(){
    return w;
}
unsigned int& State::getNumVisits(){
    return v;
}


int State::getCurrentPlayer(){ return (n3 >> 62) & 1; }

void State::switchPlayer(){
    n3 ^= 1ull << 62;
}

int State::getWinner(){
    if (n1 >> 63){
        if (n2 >> 63){
            return T;
        }
        return P1;
    }
    if (n2 >> 63){
        return P2;
    }
    return N;
}

unsigned int State::getQuadrant(const unsigned int& quadrant){
    return getQuadrant(quadrant, getCurrentPlayer());
}
unsigned int State::getQuadrant(const unsigned int& quadrant, const int& player){
    if (quadrant < 3){
        return n1 >> (9*(quadrant*2 + player));
    }
    else if (quadrant < 6){
        return n2 >> (9*((quadrant - 3)*2 + player));
    }
    else if (quadrant < 9){
        return n3 >> (9*((quadrant - 6)*2 + player));
    }
    throw "Invalid Quadrant requested";
}

int State::getPlayerAt(const unsigned int& global){
    if (global > 8){
        throw "Invalid global:  getPlayerAt";
    }
    unsigned int b1 = getBoard(0);
    unsigned int b2 = getBoard(1);
    if (IS_FILLED(b1 & b2, global)){
        cerr << "Returning Tie:  " << (b1 & 0x1ff) << " " << (b2 & 0x1ff) << " " << ((b1 & b2) & 0x1ff) << endl;
        return T;
    }
    if (IS_FILLED(b1, global)){
        return P1;
    }
    if (IS_FILLED(b2, global)){
        return P2;
    }
    return N;
}
int State::getPlayerAt(const unsigned int& global,
                       const unsigned int& local){
    if (global > 8 || local > 8){
        throw "Invalid global, local:  getPlayerAt";
    }
    if (IS_FILLED(getQuadrant(global, 0), local)){
        return P1;
    }
    if (IS_FILLED(getQuadrant(global, 1), local)){
        return P2;
    }
    return N;
}

unsigned int State::getBoard(){
    return getBoard(getCurrentPlayer()) ;
}
unsigned int State::getBoard(const int& player){
    return (player ? n1 : n2) >> 54 ;
}

unsigned int State::getGlobal(){
    return (n3 >> 54) & 0xf;
}

unsigned int State::getLocal(){
    return (n3 >> 58) & 0xf;
}

void State::setMove(const unsigned long long& global,
                     const unsigned long long& local){
    if (global > 8 || local > 8){
        throw "Invalid global, local:  setMove";
    }
            
    // clear global and local bits
    n3 &= 0xc03fffffffffffff;
    // set global and local bits
    n3 |= (global << 54) | (local << 58);
                
    // update quadrant
    if (global < 3){
        n1 |= 1ull << ((9*(global*2 + getCurrentPlayer())) + (8-local));
    }
    else if (global < 6){
        n2 |= 1ull << ((9*((global - 3)*2 + getCurrentPlayer())) + (8-local));
    }
    else if (global < 9){
        n3 |= 1ull << ((9*((global - 6)*2 + getCurrentPlayer())) + (8-local));
    }
            
    updateBoard(global, local);
            
}

void State::updateBoard(const unsigned int& global,
                         const unsigned int& local){
    if (IS_EMPTY(getBoard(0) | getBoard(1), global)){
        unsigned int quadrant = getQuadrant(global);
        if (check3InRow(local, quadrant)){
#ifdef DEBUG
            cerr << "Setting Board:  " << global << " " << getCurrentPlayer() << endl;
#endif
            if (getCurrentPlayer()){
                n1 |= 1ull << (62-global); // (8-global)+54
            }
            else{
                n2 |= 1ull << (62-global); // (8-global)+54
            }
            unsigned int bt = getBoard(0) & getBoard(1);
            if (check3InRow(global, getBoard() & ~bt)){
                if (getCurrentPlayer()){ //player 2
#ifdef DEBUG
                    cerr << "Winner P2:  " << bitset<9>(getBoard(0) & 0x1ff) << " "
                                           << bitset<9>(getBoard(1) & 0x1ff) << "  "
                                           << bitset<9>(bt) << endl;
#endif
                    n2 |= 1ull << 63;
                }
                else { // player 1
#ifdef DEBUG 
                    cerr << "Winner P2:  " << bitset<9>(getBoard(0) & 0x1ff) << " "
                                           << bitset<9>(getBoard(1) & 0x1ff) << "  "
                                           << bitset<9>(bt) << endl;
#endif
                    n1 |= 1ull << 63;                            
                }
            }
            else if (IS_TIE(getBoard(0) | getBoard(1))){ // if tie, set for both
#ifdef DEBUG
                cerr << "Winner Tie:  " << bitset<9>(getBoard(0) & 0x1ff) << " "
                                        << bitset<9>(getBoard(1) & 0x1ff) << "  "
                                        << bitset<9>(bt) << endl;
#endif
                n1 |= 1ull << 63;
                n2 |= 1ull << 63;
            }
        }
        else if (IS_TIE(getQuadrant(global, 0) | getQuadrant(global, 1))){ // if tie, set for both
#ifdef DEBUG
            cerr << "Setting Tie:  " << quadrant << endl;
#endif
            n1 |= 1ull << (62-global);
            n2 |= 1ull << (62-global);
            
            if (IS_TIE(getBoard(0) | getBoard(1))){ // if tie, set for both
#ifdef DEBUG
                cerr << "Winner Tie:  " << bitset<9>(getBoard(0) & 0x1ff) << " "
                                        << bitset<9>(getBoard(1) & 0x1ff);
#endif
                n1 |= 1ull << 63;
                n2 |= 1ull << 63;
            }
        }
    }
    else {
#ifdef DEBUG
        cerr << bitset<9>(getBoard(0) & 0x1ff) << endl;
        cerr << bitset<9>(getBoard(1) & 0x1ff) << endl;
        cerr << global << " " << local << endl;
#endif
        throw "Trying to set move in filled quadrant";
    }
}


#endif

static char getBoardSymbol(const int& player){
    switch(player){
        case P1:
            return 'X';
        case P2:
            return 'O';
        case N:
            return ' ';
        case T:
            return 'T';
        default:
            throw "Invalid player given to getBoardSymbol";
    }
}

const char* verticalSpace = "     │   │    ║    │   │    ║    │   │    ";
const char* verticalDivide = "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ";
const char* bigVerticalDivide = " ═════════════╬═════════════╬═════════════";

const char* verticalSpace2 = "    ║   ║   ";
const char* bigVerticalDivide2 = " ═══╬═══╬═══ ";
const char* minDivide = "  ";

std::ostream& operator<<(ostream& out, State* state){
    vector<string> endls (23, "");
    unsigned int i = 6;
    endls[i++] = verticalSpace2;
    ostringstream r1;
    r1 << "  ";
    for (int j = 0; j<3; ++j){
        r1 << getBoardSymbol(state->getPlayerAt(j));
        if (j != 2){
            r1 << " ║ ";
        }
    }
    r1 << " ";
    endls[i++] = r1.str();
    endls[i++] = bigVerticalDivide2;
    ostringstream r2;
    r2 << "  ";
    for (int j = 3; j<6; ++j){
        r2 << getBoardSymbol(state->getPlayerAt(j));
        if (j != 5){
            r2 << " ║ ";
        }
    }
    r2 << " ";
    endls[i++] = r2.str();
    endls[i++] = bigVerticalDivide2;
    ostringstream r3;
    r3 << "  ";
    for (int j = 6; j<9; ++j){
        r3 << getBoardSymbol(state->getPlayerAt(j));
        if (j != 8){
            r3 << " ║ ";
        }
    }
    r3 << " ";
    endls[i++] = r3.str();
    endls[i++] = verticalSpace2;
    i = 0;
    
    
    out << endl;
    for (int a = 0; a < 3; ++a) {
        if (a != 0) {
            out << bigVerticalDivide << minDivide << " " << endls[i++] << endl;
        }
        out << verticalSpace << minDivide << " " << endls[i++] << endl;
        for (int b = 0; b < 3; ++b) {
            if (b != 0) {
                out << verticalDivide << minDivide << " " << endls[i++] << endl;
            }
            out << "  ";
            for (int c = 0; c < 3; ++c) {
                if (c != 0) {
                    out << " ║ ";
                }
                for (int d = 0; d < 3; ++d) {
                    if (d != 0) {
                        out << "│";
                    }
                    out << " " << getBoardSymbol(state->getPlayerAt(3 * a + c, 3 * b + d)) << " ";
                }
            }
            out << minDivide << "  " << endls[i++] << endl;
        }
        out << verticalSpace << minDivide << " " << endls[i++] << endl;
    }
    out << endl;
    
    
#ifdef DEBUG
    out << endl << bitset<64>(state->n1) << endl;
    out << bitset<64>(state->n2) << endl;
    out << bitset<64>(state->n3) << endl << endl;
    for (int i = 0; i<9; ++i){
        out << bitset<9>(state->getQuadrant(i, 0) & 0x1ff) << "  "
            << bitset<9>(state->getQuadrant(i, 1) & 0x1ff) << endl;
    }
#endif
    
    return out;
}

