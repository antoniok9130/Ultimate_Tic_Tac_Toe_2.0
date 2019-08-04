#include <cmath>
#include <iostream>
#include <ctime>

using namespace std;

inline double UCT(const int& n, const int& v, const double& s2lpv){
    return (n+sqrt(v)*s2lpv)/v;
}

int main(){
    clock_t start = clock();
    double total = 0;
    for (int i = 100; i<2000000; ++i){
        const double s2lpv = sqrt(log(2*i*(i%5+2)));
        for (int j = 0; j<9; ++j){
            total += UCT(i+j, i*(i%5+1), s2lpv);
        }
    }
    clock_t end = clock();

    cout << total << endl;
    cout << double(end-start)/CLOCKS_PER_SEC << endl;
}