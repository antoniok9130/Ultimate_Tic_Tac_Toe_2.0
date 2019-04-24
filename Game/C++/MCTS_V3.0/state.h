#ifndef __STATE_H__
#define __STATE_H__

#define __UTTT_STORES_CHILDREN__
#define __UTTT_HAS_MEMBERS__

constexpr int N = 0;
constexpr int P1 = 1;
constexpr int P2 = 2;
constexpr int T = -1;

#define IS_EMPTY(x, y) ((((x) >> (8-y)) & 1) == 0)
#define IS_FILLED(x, y) ((((x) >> (8-y)) & 1) == 1)
#define IS_TIE(x) (((x) & 0x1ff) == 0x1ff)

#include <iostream>

class State {
    State* parent = nullptr;
    #ifdef __UTTT_STORES_CHILDREN__
    State* maxUCTChild = nullptr;
    State* children = nullptr;
    unsigned int numChildren = 0;
    #endif
    
    unsigned long w = 0; // Number of Wins
    unsigned long n = 0; // Number of Visits
    
    unsigned long long n1 = 0;
    unsigned long long n2 = 0;
    unsigned long long n3 = 0;

    /*
    n1:
        Bits 0-8 are P1 quadrant 0
        Bits 9-17 are P2 quadrant 0
        Bits 18-26 are P1 quadrant 1
        Bits 27-35 are P2 quadrant 1
        Bits 36-44 are P1 quadrant 2
        Bits 45-53 are P2 quadrant 2
        Bits 54-62 are P1 Board
        Bit 63 is 1 iff player 1 is winner
        
    n2:
        Bits 0-8 are P1 quadrant 3
        Bits 9-17 are P2 quadrant 3
        Bits 18-26 are P1 quadrant 4
        Bits 27-35 are P2 quadrant 4
        Bits 36-44 are P1 quadrant 5
        Bits 45-53 are P2 quadrant 5
        Bits 54-62 are P2 Board
        Bit 63 is 1 iff player 2 is winner
        
    n3:
        Bits 0-8 are P2 quadrant 6
        Bits 9-17 are P2 quadrant 6
        Bits 18-26 are P2 quadrant 7
        Bits 27-35 are P2 quadrant 7
        Bits 36-44 are P1 quadrant 8
        Bits 45-53 are P2 quadrant 8
        Bits 54-57 are Global Move
        Bits 58-61 are Local Move
        Bit 62 is current player; 0 if player 1; 1 if player 2
    */
    
#ifdef __UTTT_HAS_MEMBERS__
    public:
    
        State();
        State(State* parent);
        State(State* parent, const unsigned int& global,
                             const unsigned int& local);
    
        ~State();
    
        unsigned int& getNumChildren();
        State* getChildren();
        unsigned int& getNumWins();
        unsigned int& getNumVisits();
    
    
        int getCurrentPlayer();
    
        // Set player to opposite of current
        void switchPlayer();
    
        int getWinner();

        /*
        The least significant 9 bits in the integer returned 
        is the requested quadrant for the current player
        */
        unsigned int getQuadrant(const unsigned int& quadrant);
        unsigned int getQuadrant(const unsigned int& quadrant, const int& player);
    
        int getPlayerAt(const unsigned int& global);
        int getPlayerAt(const unsigned int& global,
                        const unsigned int& local);
    
        void setMove(const unsigned long long& global,
                     const unsigned long long& local);
    
        void updateBoard(const unsigned int& global,
                         const unsigned int& local);

        /*
        least significant 9 bits in returned unsigned int
        represent the board for the desired player
        */
        unsigned int getBoard();
        unsigned int getBoard(const int& player);

        unsigned int getLocal();
        unsigned int getGlobal();
#endif
    friend std::ostream& operator<<(std::ostream&, State*);
};


#endif
