#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>

#include <MCTS.h>
#include <capi.h>

using namespace std;

int main(){
    MCTS m;
    MCTS::runParallelIterations(&m, 2000000);
}
