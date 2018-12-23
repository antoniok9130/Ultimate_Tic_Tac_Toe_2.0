
#include <cassert>
#include <iostream>
#include "tests.h"
#include "Node.h"

using namespace std;

void runTests(){
    Node* node = new Node();
    Node* game = node;
    game->setChild(4, 4);
    game = game->getChild(0);
    game->init();

    assert(game->getCapturedQuadrant() == N);

    delete node;
}