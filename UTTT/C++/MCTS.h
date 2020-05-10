#pragma once

#include <iostream>
#include <memory>

#include "UTTT.h"

// #define STORE_UCT

class MCTS: public UTTT {

    MCTS* parent = nullptr;
    std::shared_ptr<MCTS[]> children = nullptr;
    int numChildren = 0;

    unsigned long w = 0; // Number of Wins
    unsigned long v = 0; // Number of Visits
#ifdef STORE_UCT
    double UCT = 100;
#endif

    public:
        MCTS();
        MCTS(const MCTS&);
        MCTS(MCTS* parent, const unsigned int global, const unsigned int local);

        // UTTT& operator=(const UTTT& other);

        void init(MCTS* parent, const unsigned int global,
                                const unsigned int local);

        MCTS* getParent();
        void setParent(MCTS* parent);

        int getNumChildren();
        std::shared_ptr<MCTS[]> getChildren();
        void allocateChildren(int numChildren);

        bool setMove(const unsigned long long global,
                     const unsigned long long local) override;

#ifdef STORE_UCT
        void setUCTbit();
        double& getUCT();
    #endif

        unsigned long getNumWins();
        unsigned long getNumVisits();
        void incrementWins();
        void incrementVisits();


        static MCTS* select(MCTS*);
        static MCTS* expand(MCTS*);
        static int simulate(MCTS*);
        static void backprop(MCTS*, int winner);
};
