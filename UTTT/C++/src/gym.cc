#include "../gym.h"

Gym::Gym(size_t batchSize):
    batchSize{batchSize},
    games{batchSize},
    moves{batchSize} {}

void Gym::reset(){
    for (auto& game : games){
        game.clear();
    }
    for (auto& move : moves){
        moves.clear();
    }
}

void Gym::save(){

}

void Gym::next(){
    int i = 0;
    for (auto& game : games){
        game.makeMove();
        moves[i++].emplace_back(
            9 * game.getGlobal() + game.getLocal()
        );
    }
}
bool Gym::isFinished(){
    for (auto& game : games){
        if (!game.isFinished()){
            return false;
        }
    }
    return true;
}

Gym::Leaves::Leaves(size_t numLeaves){
    leaves.reserve(numLeaves);
}

std::unique_ptr<int[]> Gym::Leaves::toTensor(){
    int* tensor = new int [leaves.size() * 9 * 3 * 3];
    int* data = tensor;
    for(auto leaf : leaves){
        for (int q = 0; q < 9; ++q){
            leaf->fillArray(data, q);
            data += 9;
        }
    }
    return std::unique_ptr<int[]>(tensor);
}

Gym::Leaves Gym::getLeaves(){
    Leaves leaves{batchSize};

    for (auto& game : games){
        leaves.leaves.emplace_back(
            MCTS::select_expand(&game)
        );
    }

    return leaves;
}
