#pragma once

#include <atomic>
#include <iostream>
#include <memory>

#include "UTTT.h"

// #define STORE_UCT

#if defined(ROOT_PARALLEL) && defined(_OPENMP)
typedef std::atomic_ulong ULong;
typedef std::atomic_int Int;
#else
typedef unsigned long ULong;
typedef int Int;
#endif

class MCTS: public UTTT {

    MCTS* parent = nullptr;
    std::shared_ptr<MCTS[]> children = nullptr;
    Int numChildren = 0;

    ULong w = 0; // Number of Wins
    ULong v = 0; // Number of Visits
#ifdef STORE_UCT
    double UCT = 100;
#endif

    public:
        MCTS();
        MCTS(MCTS&);
        MCTS(MCTS* parent, const unsigned int global, const unsigned int local);

        MCTS& operator=(const MCTS& other);

        void init(MCTS* parent, const unsigned int global,
                                const unsigned int local);

        MCTS* getParent();
        void setParent(MCTS* parent);

        int getNumChildren();
        std::shared_ptr<MCTS[]> getChildren();
        bool allocateChildren(int numChildren);  // returns true iff allocated

        MCTS* bestChild();
        MCTS* mostVisitedChild();
        void makeMove();
        void chooseMove(const unsigned int quadrant, const unsigned int local);

#ifdef STORE_UCT
        void setUCTbit();
        double& getUCT();
    #endif

        unsigned long getNumWins();
        unsigned long getNumVisits();
        void incrementWins(int amount = 1);
        void incrementVisits(int amount = 1);

        static MCTS* select(MCTS*);
        static MCTS* expand(MCTS*);
        static int simulate(MCTS*);
        static void backprop(MCTS*, int winner);

        static MCTS* select_expand(MCTS*);
        static void runIterations(MCTS*, int numIterations);

        void save(const char* path, bool append=true);
};
