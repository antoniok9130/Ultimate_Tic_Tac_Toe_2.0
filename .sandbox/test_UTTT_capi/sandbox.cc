#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>
#include <chrono>

#include <MCTS.h>
#include <UTTT.h>
#include <capi.h>

using namespace std;

int main(){
    MCTS m;
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    MCTS::runIterations(&m, 2000000);

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

    cout << "duration: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count()/1000.0 << " seconds" << endl;
}
