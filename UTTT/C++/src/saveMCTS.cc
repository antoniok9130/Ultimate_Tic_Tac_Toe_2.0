#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>

#include "../MCTS.h"

using namespace std;

void MCTS::save(const char* path, bool append){

    int8_t length = 0;
    int8_t moves[81][2];

    MCTS* current = this;
    while (current){
        moves[length][0] = current->getGlobal();
        moves[length][1] = current->getLocal();
        ++length;
        current = current->getParent();
    }

    auto options = ios::out | ios::binary;
    if (append){
        options |= ios::app;
    }
    ofstream file (path, options);
    if (file.fail()){
        throw ios_base::failure(strerror(errno));
    }
    file.exceptions(file.exceptions() | ios::failbit | ifstream::badbit);

    file << length;
    for (int8_t i = length-1; i >= 0; --i){
        if (i < length-1 && moves[i+1][1] != moves[i][0]){
            file << moves[i][0];
        }
        file << moves[i][1];
    }
    file << n1;
    file << n2;
    file << n3;
    file << endl;

}
