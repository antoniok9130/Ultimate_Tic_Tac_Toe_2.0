#include <iostream>
#include <cstdlib>
#include <ctime>

#include <UTTT.h>
#include <utils.h>

using namespace std;

template<typename RET, typename... Args>
void timeit(int iterations, RET (*f)(Args...), Args&&... args){
    std::clock_t start = std::clock();

    for (int i = 0; i<iterations; ++i){
        f(args...);
    }

    double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;

    cout << "iterations: " << iterations << endl;
    if (duration > 1){
        cout << "time: " << duration << " seconds" << endl;
    }
    else {
        cout << "time: " << duration * 1000.0 << " milliseconds" << endl;
    }
    cout << duration / iterations * 1000 << " milliseconds per iteration" << endl;
}

void test_rotate(UTTT& uttt){
    rotate_270_ccw(uttt);
    rotate_90_cw(uttt);
    rotate_270_cw(uttt);
    rotate_180_ccw(uttt);
    rotate_90_ccw(uttt);
    rotate_180_cw(uttt);
}

int main(){
    UTTT uttt;

    uttt.setMove(0, 1);
    uttt.setMove(1, 2);
    uttt.setMove(2, 3);
    uttt.setMove(3, 4);
    uttt.setMove(4, 5);
    uttt.setMove(5, 6);
    uttt.setMove(6, 7);
    uttt.setMove(7, 8);
    uttt.setMove(8, 0);
    cout << uttt << endl;

    timeit(1000000, test_rotate, uttt);

    cout << uttt << endl;
}
