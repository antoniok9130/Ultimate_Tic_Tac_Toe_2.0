#pragma once

#include <memory>
#include <vector>

#include "MCTS.h"

/*
 * Gym class that provides the environment used for training a model
 */
class Gym {
    size_t batchSize;
    std::vector<MCTS> games;
    std::vector<std::vector<int>> moves;

    public:
        Gym(size_t batchSize);

        void reset();
        void save();

        void next();
        bool isFinished();

        struct Leaves {
            std::vector<MCTS*> leaves;

            Leaves(size_t numLeaves);

            std::unique_ptr<int[]> toTensor();
        };
        Leaves getLeaves();
};
