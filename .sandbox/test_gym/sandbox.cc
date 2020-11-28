#include "../utils.h"
#include "../../UTTT/C++/gym.h"

using namespace std;

void time_gym(Gym& gym) {
    for (int i = 0; i < 1; ++i){
        auto leaves = gym.getLeaves();
        auto tensor = leaves.toTensor();
    }
}

int main(){
    srand(time(NULL));
    Gym gym{4096};
    timeit(1025, time_gym, gym);
}
