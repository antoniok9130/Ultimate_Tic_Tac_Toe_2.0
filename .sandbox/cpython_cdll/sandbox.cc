#include <iostream>
#include <cstdlib>
#include <ctime>
#include <memory>

using namespace std;

struct TestStruct {
    int n = 0;

    TestStruct(){
        cout << "TestStruct:  " << this << endl;
    }

    int incrementN(){
        n++;
        return n;
    }
};

extern "C" {
    TestStruct* new_TestStruct(){ return new TestStruct(); }
    void delete_TestStruct(TestStruct* ts){ delete ts; }
    int TestStruct_incrementN(TestStruct* ts){
        if (ts <= 0){
            return -1;
        }
        return ts->incrementN();
    }
}
