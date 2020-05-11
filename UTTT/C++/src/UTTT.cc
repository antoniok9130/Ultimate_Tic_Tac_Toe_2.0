#include <bitset>
#include <cmath>
#include <exception>
#include <iostream>
#include <sstream>
#include <string>

#include "../UTTT.h"

using namespace std;

#define F9 0x1ff // Gets first 9 bits

#ifdef __UTTT_HAS_MEMBERS__

UTTT::UTTT(){}
UTTT::UTTT(const UTTT& other):
    n1 {other.n1},
    n2 {other.n2},
    n3 {other.n3}{}


bool UTTT::empty(){ return ((n1 | n2 | n3) & 0x1fffffffffffff) == 0; }


#define GET_BOARD(p) ((p ? n2 : n1) >> 54)
#define GET_BOARD_P1 (n1 >> 54)
#define GET_BOARD_P2 (n2 >> 54)
#define GET_BOARD_OR ((n1 | n2) >> 54)
#define GET_CURRENT_PLAYER ((n3 >> 62) & 1)

int UTTT::getCurrentPlayer(){ return GET_CURRENT_PLAYER; }
/*
setCurrentPlayer:  p == true iff P2
*/
void UTTT::setCurrentPlayer(const bool p){
    if (p){
        n3 |= (1ull << 62); // 0x4000000000000000; //
    } else{
        n3 &= ~(1ull << 62); // 0xbfffffffffffffff; //
    }
}

void UTTT::switchPlayer(){
    n3 ^= 1ull << 62; // 0x4000000000000000; //
}

int UTTT::getWinner(){
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

unsigned int UTTT::getQuadrant(const unsigned int quadrant){
    return getQuadrant(quadrant, GET_CURRENT_PLAYER);
}
unsigned int UTTT::getQuadrant(const unsigned int quadrant, const int player){
    if (quadrant < 3){
        return n1 >> (9*(quadrant*2 + player));
    }
    else if (quadrant < 6){
        return n2 >> (9*((quadrant - 3)*2 + player));
    }
    else if (quadrant < 9){
        return n3 >> (9*((quadrant - 6)*2 + player));
    }
    cerr << "Requested Quadrant: " << quadrant << endl;
    throw runtime_error("Invalid Quadrant requested");
}

int UTTT::getPlayerAt(const unsigned int global){
    if (global > 8){
        throw runtime_error("Invalid global:  getPlayerAt");
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
int UTTT::getPlayerAt(const unsigned int quadrant,
                      const unsigned int local){
    if (quadrant > 8 || local > 8){
        throw runtime_error("Invalid global, local:  getPlayerAt");
    }
    if (IS_FILLED(getQuadrant(quadrant, 0), local)){
        return P1;
    }
    if (IS_FILLED(getQuadrant(quadrant, 1), local)){
        return P2;
    }
    return N;
}

unsigned int UTTT::getBoard(){
    return GET_BOARD(GET_CURRENT_PLAYER) ;
}
unsigned int UTTT::getBoard(const int player){
    return GET_BOARD(player) ;
}

unsigned int UTTT::getGlobal(){
    return (n3 >> 54) & 0xf;
}

unsigned int UTTT::getLocal(){
    return (n3 >> 58) & 0xf;
}

bool UTTT::setMove(const unsigned long long quadrant,
                   const unsigned long long local){
    if (quadrant > 8 || local > 8){
        throw runtime_error("Invalid quadrant, local:  setMove");
    }

    // clear global and local bits
    n3 &= 0xc03fffffffffffff;
    // set global and local bits
    n3 |= (quadrant << 54) | (local << 58);

    // update quadrant
    if (quadrant < 3){
        n1 |= 1ull << ((9*(quadrant*2 + GET_CURRENT_PLAYER)) + local);
    }
    else if (quadrant < 6){
        n2 |= 1ull << ((9*((quadrant - 3)*2 + GET_CURRENT_PLAYER)) + local);
    }
    else if (quadrant < 9){
        n3 |= 1ull << ((9*((quadrant - 6)*2 + GET_CURRENT_PLAYER)) + local);
    }
    return updateBoard(quadrant, local);
}

bool UTTT::updateBoard(const unsigned int global,
                       const unsigned int local){
    if (IS_EMPTY(GET_BOARD_OR, global)){
        unsigned int quadrant = getQuadrant(global);
        if (check3InRow(quadrant, local)){
            bool player = GET_CURRENT_PLAYER;
            if (player){
                n2 |= 1ull << (54+global);
            }
            else{
                n1 |= 1ull << (54+global);
            }
            unsigned long boards[2] = {GET_BOARD_P1, GET_BOARD_P2};
            if (check3InRow(boards[player] & ~boards[!player], global)){
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
            n1 |= 1ull << (54+global);
            n2 |= 1ull << (54+global);
            if (IS_TIE(GET_BOARD_P1 | GET_BOARD_P2)){ // if tie, set for both
                n1 |= 1ull << 63; // 0x8000000000000000; //
                n2 |= 1ull << 63; // 0x8000000000000000; //
            }
            return true;
        }
    }
    else {
        cout << *this << endl << endl;

        cout << "n1: " << (n1 >> 63) << " ";
        for (int i = 54; i >= 0; i -= 9){
            cout << bitset<9>((n1 >> i) & 0x1FF) << " ";
        }
        cout << endl;

        cout << "n2: " << (n2 >> 63) << " ";
        for (int i = 54; i >= 0; i -= 9){
            cout << bitset<9>((n2 >> i) & 0x1FF) << " ";
        }
        cout << endl;

        cout << "n3: " << (n3 >> 63) << " ";
        cout << ((n3 >> 62) & 1) << " ";
        cout << ((n3 >> 58) & 0xF) << " ";
        cout << ((n3 >> 54) & 0xF) << " ";
        for (int i = 45; i >= 0; i -= 9){
            cout << bitset<9>((n3 >> i) & 0x1FF) << " ";
        }
        cout << endl;

        throw runtime_error("Trying to set move in filled quadrant");
    }
    return false;
}


#endif


bool UTTT::check3InRow(const unsigned int quadrant, const unsigned int local){
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
}
