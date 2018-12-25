//
// Created by Antonio on 2018-04-18.
//

#include "Node.h"
#include <cmath>
#include <iostream>
#include <sstream>
#include "Game.h"

using namespace std;

int n_seed = time(NULL);
inline int fastrand() {
    n_seed = (214013 * n_seed + 2531011);
    return (n_seed >> 16) & 0x7FFF;
}

NodePool::NodePool(const size_t& max_size): max_size{max_size} {
    cout << "Initializing Game..." << endl;
    pool = new Node*[max_size];
    for (size_t i = 0; i<max_size; ++i){
        pool[i] = new Node();
        stack.emplace_back(pool[i]);
    }
    cout << "Initialized Game." << endl;
}
NodePool::~NodePool(){
    stack.clear();
    for (size_t i = 0; i<max_size; ++i){
        delete pool[i];
    }
    delete[] pool;
}
Node* NodePool::getNode(){
    auto& instance = NodePool::getInstance(0);
    if (instance.stack.empty()){
        return nullptr;
    }
    Node* node = instance.stack.front();
    instance.stack.pop_front();
    return node;
}
void NodePool::returnNode(Node* node){
    if (!node->getChildren().empty()){
        for (auto child : node->getChildren()){
            returnNode(child);
        }
    }
    NodePool::getInstance(0).stack.emplace_back(node);
}
size_t NodePool::maxSize(){
    return NodePool::getInstance(0).max_size;
}
size_t NodePool::size(){
    return NodePool::getInstance(0).stack.size();
}
bool NodePool::empty(){
    return NodePool::getInstance(0).stack.empty();
}

Node::Node() {}

void Node::reset(){
    winner = N;
    player = N;
    nextQuadrant = -1;
    numVisits = 0;
    numWins = 0;
    length = 0;
    UCT = fastrand()%243+10;
    oldUCT = false;
    local = -1;
    global = -1;
    moveSet = false;
    capturedQuadrant = N;
    parent = nullptr;
    numChildren = 0;
    children.clear();
    initialized = false;
}
void Node::init(const int& global, const int& local, Node* parent, const bool& initialize){
    reset();
    this->parent = parent;
    if (parent){
        winner = parent->winner;
        player = other(parent->player);
        length = parent->length + 1;
        setMove(global, local);

        if (moveSet && !capturedQuadrantEquals(local, true)) {
            nextQuadrant = local;
        }
        if (initialize){
            if (winner == N){
                init();
            }
            else{
                initialized = true;
            }
        }
    }
    else{
        player = P1;
        length = 1;
        initialized = true;
    }
}

void Node::init() {
    if (!initialized) {
        if (moveSet) { 
            Quadrant currentQuadrant = make_Quadrant();
            buildQuadrant(currentQuadrant, global);
            if (check3InRow(currentQuadrant, global)) {
                capturedQuadrant = player;
                Quadrant allQuadrants = make_Quadrant();
                buildQuadrant(allQuadrants);
                if (check3InRow(allQuadrants, global)){
                    winner = player;
                }
            }
            // Quadrant currentQuadrant = make_Quadrant();
            // buildQuadrant(currentQuadrant, global);
            // int filled = check3InRow(currentQuadrant);
            // if (filled != N) {
            //     capturedQuadrant = filled;
            //     Quadrant allQuadrants = make_Quadrant();
            //     buildQuadrant(allQuadrants);
            //     winner = check3InRow(allQuadrants);
            // }
            initialized = true;
        }
    }
}

bool Node::isLegal(const std::unique_ptr<Move>& move) {
    return isLegal(move->first, move->second);
}
bool Node::isLegal(const int& global, const int& local) {
    return (nextQuadrant == -1 || global == nextQuadrant) && !moveOrCapturedQuadrantEquals(global, local, global);
    // quadrants->remainingContains(move->first) && (nextQuadrant == -1 || move->first == nextQuadrant) &&
    //     board->remainingContains(move);
}

bool Node::hasMove() { return moveSet; }
unique_ptr<Move> Node::getMove() { return make_unique<Move>(global, local); }
void Node::setMove(const unique_ptr<Move>& move) {
    setMove(move->first, move->second);
}
void Node::setMove(const int& global, const int& local) {
    if (!moveSet){
        if (0 <= global && global <= 8 && 0 <= local && local <= 8){
            moveSet = true;
        }
        this->global = global;
        this->local = local;
    }
}

int Node::getGlobal() { return moveSet ? global : -1; }
int Node::getLocal() { return moveSet ? local : -1; }
int Node::getWinner() { return winner; }
int Node::getNextQuadrant() { return nextQuadrant; }
int Node::getCapturedQuadrant() { return capturedQuadrant; }

bool Node::moveEquals(const int& global, const int& local) {
    return (moveSet && this->global == global && this->local == local);
}
bool Node::capturedQuadrantEquals(const int& quadrant, const bool& backpropogate) {
    return (capturedQuadrant != N && moveSet && global == quadrant) ||
           (backpropogate && parent ? parent->capturedQuadrantEquals(quadrant, backpropogate) : false);
}
bool Node::moveOrCapturedQuadrantEquals(const int& global, const int& local, const int& quadrant) {
    return moveEquals(global, local) || capturedQuadrantEquals(quadrant) ||
           (parent ? parent->moveOrCapturedQuadrantEquals(global, local, quadrant) : false);
}

double Node::getUCT(){ 
    if (oldUCT && parent && numVisits != 0) {
        UCT = numWins / (double)numVisits + sqrt(2 * log(parent->numVisits) / numVisits);
        oldUCT = false;
    }
    return UCT;
}
int Node::getNumWins() { return numWins; }
int Node::getNumVisits() { return numVisits; }
void Node::incrementWins(const int& i) { 
    numWins += i;
    oldUCT = true;
}
void Node::incrementVisits(const int& i) { 
    numVisits += i;
    oldUCT = true;
}

int Node::getLength() { return length; }

// void Node::merge(const Node& node) {
    // if (!parent || (move && move->first == node.move->first && move->second == node.move->second)) {
    //     numWins += node.numWins;
    //     numVisits += node.numVisits;
    //     if (children.empty()) {
    //         children = node.children;
    //         numChildren = node.numChildren;
    //     } else if (!node.children.empty()) {
    //         if (children.size() == node.children.size()) {
    //             for (size_t i = 0; i < children.size(); ++i) {
    //                 children[i]->merge(*node.children[i]);
    //             }
    //         } else {
    //             throw "Children length not same.";
    //         }
    //     }
    // }
// }

int Node::getPlayer() { return player; }
Node* Node::getParent() { return parent; }
void Node::setNumChildren(unsigned int num) {
    children.clear();
    children.reserve(num);
}
bool Node::hasNoChildren() { return children.empty(); }
vector<Node*>& Node::getChildren() { return children; }
Node* Node::getChild(const int& i) { return children[i]; }
void Node::addChild(Node* move) { children.emplace_back(move); }
void Node::setChild(const unique_ptr<Move>& move) { setChild(move->first, move->second); }
void Node::setChild(const int& global, const int& local) {
    for (auto& child : children) {
        if (child->global == global && child->local == local) {
            Node* keepChild = child;
            for (size_t i = 0; i<children.size(); ++i){
                if (children[i] != keepChild){
                    NodePool::returnNode(children[i]);
                }
            }
            children.clear();
            children.emplace_back(keepChild);
            return;
        }
    }
    if (isLegal(global, local) && !NodePool::empty()) {
        for (size_t i = 0; i<children.size(); ++i){
            NodePool::returnNode(children[i]);
        }
        children.clear();
        Node* node = NodePool::getNode();
        node->init(global, local, this, true);
        children.emplace_back(node);
        return;
    }
    ostringstream err;
    err << "Could not find child with move:  " << global << " " << local;
    throw err.str();
}

void Node::buildQuadrant(Quadrant& array) {
    Node* current = this;
    do {
        if (current->capturedQuadrant != N) {
            array[current->global] = current->capturedQuadrant;
        }
        current = current->parent;
    } while (current != nullptr);
}
void Node::buildQuadrant(Quadrant& array, const int& quadrant) {
    Node* current = this;
    do {
        if (current->moveSet && current->global == quadrant) {
            array[current->local] = current->player;
        }
        current = current->parent;
    } while (current != nullptr);
}
void Node::buildBoard2D(Board2D& array) {
    Node* current = this;
    do {
        if (current->moveSet) {
            array[current->global][current->local] = current->player;
        }
        current = current->parent;
    } while (current != nullptr);
}

std::ostream& Node::printTrace(std::ostream& out) {
    if (parent) {
        parent->printTrace(out);
    }
    if (moveSet) {
        out << global << local;
    }
    return out;
}

// Quadrants& Node::getQuadrants() { return *quadrants; }

// Board2D& Node::getBoard() { return *board; }

// ostream& operator<<(ostream& out, Node& node) {
//     out << node.getQuadrants() << endl;
//     out << node.getBoard() << endl;
//     return out;
// }

// Node* Node_new() { return new Node(); }
// void Node_delete(Node* node) { delete node; }
// int Node_getWinner(Node* node) { return node->getWinner(); }
// int Node_getNumWins(Node* node) { return node->getNumWins(); }
// int Node_getNumVisits(Node* node) { return node->getNumVisits(); }