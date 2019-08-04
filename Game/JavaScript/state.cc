#include "state.h"
#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>
#include <bitset>

using namespace std;

#define F9 0x1ff // Gets first 9 bits

bool check3InRow(const unsigned int& local,
                 const unsigned int& quadrant){
#ifdef REVERSE_BOARD
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
#else
    switch(local){
        case 0:
            return ((quadrant & 0b000000111) == 0b000000111) ||
                   ((quadrant & 0b001001001) == 0b001001001) ||
                   ((quadrant & 0b100010001) == 0b100010001);
        case 1:
            return ((quadrant & 0b000000111) == 0b000000111) ||
                   ((quadrant & 0b010010010) == 0b010010010);
        case 2:
            return ((quadrant & 0b000000111) == 0b000000111) ||
                   ((quadrant & 0b100100100) == 0b100100100) ||
                   ((quadrant & 0b001010100) == 0b001010100);
        case 3:
            return ((quadrant & 0b001001001) == 0b001001001) ||
                   ((quadrant & 0b000111000) == 0b000111000);
        case 4:
            return ((quadrant & 0b100010001) == 0b100010001) ||
                   ((quadrant & 0b010010010) == 0b010010010) ||
                   ((quadrant & 0b001010100) == 0b001010100) ||
                   ((quadrant & 0b000111000) == 0b000111000);
        case 5:
            return ((quadrant & 0b100100100) == 0b100100100) ||
                   ((quadrant & 0b000111000) == 0b000111000);
        case 6:
            return ((quadrant & 0b111000000) == 0b111000000) ||
                   ((quadrant & 0b001010100) == 0b001010100) ||
                   ((quadrant & 0b001001001) == 0b001001001);
        case 7:
            return ((quadrant & 0b010010010) == 0b010010010) ||
                   ((quadrant & 0b111000000) == 0b111000000);
        case 8:
            return ((quadrant & 0b111000000) == 0b111000000) ||
                   ((quadrant & 0b100010001) == 0b100010001) ||
                   ((quadrant & 0b100100100) == 0b100100100);
        default:
            return false;
    }
#endif
}

#ifdef __UTTT_HAS_MEMBERS__

State::State(){}
State::State(State* other):
    parent {other->parent},
    #ifdef __UTTT_STORES_CHILDREN__
    children {other->children},
    numChildren {other->numChildren},
    #endif
    w {other->w},
    v {other->v},
    #ifdef STORE_UCT
    UCT {other->UCT},
    #endif
    n1 {other->n1},
    n2 {other->n2},
    n3 {other->n3}{}
State::State(State* parent, const unsigned int& global,
                             const unsigned int& local):
    parent {parent},
    n1 {parent->n1},
    n2 {parent->n2},
    n3 {parent->n3}{
    setCurrentPlayer(1-parent->getCurrentPlayer());
    setMove(global, local);
}
State::~State(){
    #ifdef __UTTT_STORES_CHILDREN__
    if (children){
        if (numChildren == -1){
            delete children;
        }
        else{
            delete[] children;
        }
    }
    #endif
}
State& State::operator=(const State& other){
    #ifdef __UTTT_STORES_CHILDREN__
    if (children){
        if (numChildren == -1){
            delete children;
        }
        else{
            delete[] children;
        }
    }
    children = other.children;
    numChildren = other.numChildren;
    #endif
    
    parent = other.parent;
    w = other.w;
    v = other.v;
    #ifdef STORE_UCT
    UCT = other.UCT;
    #endif
    n1 = other.n1;
    n2 = other.n2;
    n3 = other.n3;
    
    return *this;
}
void State::init(State* parent, const unsigned int& global,
                                const unsigned int& local){
    this->parent = parent;
    n1 = parent->n1;
    n2 = parent->n2;
    n3 = parent->n3;
    setCurrentPlayer(1-parent->getCurrentPlayer());
    setMove(global, local);
}


State* State::getParent(){
    return parent;
}
void State::setParent(State* parent){
    this->parent = parent;
}
int& State::getNumChildren(){
     return numChildren;
}
State* State::getChildren(){
    return children;
}
void State::setChildren(State* s){
    children = s;
}
unsigned long& State::getNumWins(){
    return w;
}
unsigned long& State::getNumVisits(){
    return v;
}
#ifdef STORE_UCT
void State::setUCTbit(){
    n3 |= (1ull << 63); // 0x8000000000000000; // 
}
double& State::getUCT(){
    if (n3 >> 63){
        UCT = v == 0 ? 100 : (parent ? (w+sqrt(2*v*log(parent->v)))/v : double(w)/v);
        n3 &= ~(1ull << 63); // 0x7fffffffffffffff; // 
    }
    return UCT;
}
#endif

bool State::empty(){ return ((n1 | n2 | n3) & 0x1fffffffffffff) == 0; }


#define GET_BOARD(p) ((p ? n2 : n1) >> 54)
#define GET_BOARD_P1 (n1 >> 54)
#define GET_BOARD_P2 (n2 >> 54)
#define GET_CURRENT_PLAYER ((n3 >> 62) & 1)

int State::getCurrentPlayer(){ return GET_CURRENT_PLAYER; }
/*
setCurrentPlayer:  p == true iff P2
*/
void State::setCurrentPlayer(const bool& p){
    if (p){
        n3 |= (1ull << 62); // 0x4000000000000000; // 
    } else{
        n3 &= ~(1ull << 62); // 0xbfffffffffffffff; // 
    }
}

void State::switchPlayer(){
    n3 ^= 1ull << 62; // 0x4000000000000000; // 
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
    return getQuadrant(quadrant, GET_CURRENT_PLAYER);
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
    unsigned int b1 = GET_BOARD_P1;
    unsigned int b2 = GET_BOARD_P2;
    if (IS_FILLED(b1 & b2, global)){
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
    return GET_BOARD(GET_CURRENT_PLAYER) ;
}
unsigned int State::getBoard(const int& player){
    return GET_BOARD(player) ;
}

unsigned int State::getGlobal(){
    return (n3 >> 54) & 0xf;
}

unsigned int State::getLocal(){
    return (n3 >> 58) & 0xf;
}

bool State::setMove(const unsigned long long& global,
                     const unsigned long long& local){
    if (global > 8 || local > 8){
        throw "Invalid global, local:  setMove";
    }
    
    if (numChildren > 0){
        for (int i = 0; i<numChildren; ++i){
            if (children[i].getGlobal() == global && 
                children[i].getLocal() == local){
                State child {children+i};
                children[i].children = nullptr;
                *this = child;
                child.children = nullptr;
                parent = nullptr;
                for (i = 0; i<numChildren; ++i){
                    children[i].parent = this;
                }
                return false;
            }
        }
    }
            
    // clear global and local bits
    n3 &= 0xc03fffffffffffff;
    // set global and local bits
    n3 |= (global << 54) | (local << 58);
                
    // update quadrant
#ifdef REVERSE_BOARD
    if (global < 3){
        n1 |= 1ull << ((9*(global*2 + GET_CURRENT_PLAYER)) + (8-local));
    }
    else if (global < 6){
        n2 |= 1ull << ((9*((global - 3)*2 + GET_CURRENT_PLAYER)) + (8-local));
    }
    else if (global < 9){
        n3 |= 1ull << ((9*((global - 6)*2 + GET_CURRENT_PLAYER)) + (8-local));
    }
#else
    if (global < 3){
        n1 |= 1ull << ((9*(global*2 + GET_CURRENT_PLAYER)) + local);
    }
    else if (global < 6){
        n2 |= 1ull << ((9*((global - 3)*2 + GET_CURRENT_PLAYER)) + local);
    }
    else if (global < 9){
        n3 |= 1ull << ((9*((global - 6)*2 + GET_CURRENT_PLAYER)) + local);
    }
#endif
            
    return updateBoard(global, local); 
}

bool State::updateBoard(const unsigned int& global,
                         const unsigned int& local){
    if (IS_EMPTY(GET_BOARD_P1 | GET_BOARD_P2, global)){
        unsigned int quadrant = getQuadrant(global);
        if (check3InRow(local, quadrant)){
            bool player = GET_CURRENT_PLAYER;
#ifdef REVERSE_BOARD
            if (player){
                n2 |= 1ull << (62-global);
            }
            else{
                n1 |= 1ull << (62-global);
            }
#else
            if (player){
                n2 |= 1ull << (54+global);
            }
            else{
                n1 |= 1ull << (54+global);
            }
#endif
            unsigned long long boards[2] = {GET_BOARD_P1, GET_BOARD_P2};
            if (check3InRow(global, boards[player] & ~boards[!player])){
//                 cout << "Winner:  " << player << endl;
                if (player){ //player 2
                    n2 |= 1ull << 63; // 0x8000000000000000; // 
                }
                else { // player 1
                    n1 |= 1ull << 63; // 0x8000000000000000; //                 
                }
            }
            else if (IS_TIE(boards[0] | boards[1])){ // if tie, set for both
//                 cout << "Winner:  Tie" << endl;
                n1 |= 1ull << 63; // 0x8000000000000000; // 
                n2 |= 1ull << 63; // 0x8000000000000000; // 
            }
            return true;
        }
        else if (IS_TIE(getQuadrant(global, 0) | getQuadrant(global, 1))){ // if tie, set for both
#ifdef REVERSE_BOARD
            n1 |= 1ull << (62-global);
            n2 |= 1ull << (62-global);
#else
            n1 |= 1ull << (54+global);
            n2 |= 1ull << (54+global);
#endif
            
            if (IS_TIE(GET_BOARD_P1 | GET_BOARD_P2)){ // if tie, set for both
                n1 |= 1ull << 63; // 0x8000000000000000; // 
                n2 |= 1ull << 63; // 0x8000000000000000; // 
            }
            return true;
        }
    }
    else {
        cout << *this << endl;
        cout << endl << bitset<64>(n1) << endl;
        cout << bitset<64>(n2) << endl;
        cout << bitset<64>(n3) << endl;
        cout << global << " " << local << endl << endl;
        cout << "Trying to set move in filled quadrant" << endl;
        throw "Trying to set move in filled quadrant";
    }
    return false;
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

std::ostream& operator<<(ostream& out, State& state){
    vector<string> endls (23, "");
    unsigned int i = 6;
    endls[i++] = verticalSpace2;
    ostringstream r1;
    r1 << "  ";
    for (int j = 0; j<3; ++j){
        r1 << getBoardSymbol(state.getPlayerAt(j));
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
        r2 << getBoardSymbol(state.getPlayerAt(j));
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
        r3 << getBoardSymbol(state.getPlayerAt(j));
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
                    out << " " << getBoardSymbol(state.getPlayerAt(3 * a + c, 3 * b + d)) << " ";
                }
            }
            out << minDivide << "  " << endls[i++] << endl;
        }
        out << verticalSpace << minDivide << " " << endls[i++] << endl;
    }
    out << endl;
    
    
#ifdef CHECK_DEPTH
    out << endl << bitset<64>(state.n1) << endl;
    out << bitset<64>(state.n2) << endl;
    out << bitset<64>(state.n3) << endl << endl;
//     for (int i = 0; i<9; ++i){
//         out << bitset<9>(state.getQuadrant(i, 0) & 0x1ff) << "  "
//             << bitset<9>(state.getQuadrant(i, 1) & 0x1ff) << endl;
//     }
#endif
    
    return out;
}

