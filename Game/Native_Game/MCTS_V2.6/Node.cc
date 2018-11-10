//
// Created by Antonio on 2018-04-18.
//

#include "Node.h"
#include <cmath>
#include <ctime>
#include <iostream>
#include <sstream>
#include "Game.h"

using namespace std;

Node::Node() {}

// Node::Node(const Node& other)
//     : winner{other.winner},
//       player{other.player},
//       nextQuadrant{-1},
//       numVisits{0},
//       numWins{0},
//       UCT{100},
//       capturedQuadrant{-1},
//       parent{other.parent},
//       quadrants{make_unique<Quadrants>(other.quadrants)},
//       board{make_unique<Board2D>(other.board)},
//       numChildren{other.numChildren},
//       children{other.children},
//       initialized{true},
//       moveSet{false} {}

// Node::Node(const s_int& moveGlobal, const s_int& moveLocal, Node* parent, const bool& initialize)
//     : Node{Move{moveGlobal, moveLocal}, parent, initialize} {}
Node::Node(Move* move, Node* parent, const bool& initialize)
    : winner{parent ? parent->winner : N},
    //   player{parent ? (parent->player == P1 ? P2 : P1) : P1},
      length{parent ? (parent->length + 1) : 0},
      move{move},
      parent{parent},
      initialized{parent ? false : true} {
    if (parent) {
        if (this->move && !capturedQuadrantEquals(this->move->second, true)) {
            nextQuadrant = this->move->second;
        }
        if (initialize) {
            if (this->winner == N) {
                init();
            } else {
                // this->quadrants = make_unique<Quadrants>(parent->quadrants);
                // this->board = make_unique<Board2D>(parent->board);
                initialized = true;
            }
        }
    }
}

void Node::init() {
    if (!initialized) {
        if (move) {
            setMove();
        }
        // else {
        //     move = make_unique<Move>(*parent->move);
        // }
        initialized = true;
    }
}

// void Node::updateUCT() {
//     if (parent && numVisits != 0) {
//         UCT = numWins / (double)numVisits + sqrt(2 * log(parent->numVisits) / numVisits);
//     }
// }

bool Node::isLegal(const Move& move) {
    return (nextQuadrant == -1 || move.first == nextQuadrant) && !moveOrCapturedQuadrantEquals(move, move.first);
    // quadrants->remainingContains(move->first) && (nextQuadrant == -1 || move->first == nextQuadrant) &&
    //     board->remainingContains(move);
}

bool Node::hasMove() { return move ? true : false; }
Move* Node::getMove() { return move; }
// void Node::setMove(int moveGlobal, int moveLocal) {
//     if (!this->move) {
//         this->move = make_unique<int, int>(std::move(moveGlobal), std::move(moveLocal));
//         setMove();
//     }
// }
// void Node::setMove(unique_ptr<Move>& move) {
//     if (this->move == nullptr) {
//         this->move = std::move(move);
//         setMove();
//     }
// }
void Node::setMove() {
    if (move && !moveSet) {
        Quadrant currentQuadrant = make_Quadrant();
        buildQuadrant(currentQuadrant, move->first);
        if (check3InRow(currentQuadrant, move->second)) {
            const s_int player = length%2 == 0 ? P2 : P1;
            capturedQuadrant = player;
            Quadrant allQuadrants = make_Quadrant();
            buildQuadrant(allQuadrants);
            if (check3InRow(allQuadrants, move->first)){
                winner = player;
            }
        }
        moveSet = true;
    }
}

s_int Node::getGlobal() { return move ? move->first : -1; }
s_int Node::getLocal() { return move ? move->second : -1; }
s_int Node::getWinner() { return winner; }
s_int Node::getNextQuadrant() { return nextQuadrant; }
s_int Node::getCapturedQuadrant() { return capturedQuadrant; }

bool Node::moveEquals(const Move& move) {
    return (this->move && this->move->first == move.first && this->move->second == move.second);
}
bool Node::capturedQuadrantEquals(const int& quadrant, const bool& backpropogate) {
    return (capturedQuadrant != N && move && move->first == quadrant) ||
           (backpropogate && parent ? parent->capturedQuadrantEquals(quadrant, backpropogate) : false);
}
bool Node::moveOrCapturedQuadrantEquals(const Move& move, const int& quadrant) {
    return moveEquals(move) || capturedQuadrantEquals(quadrant) ||
           (parent ? parent->moveOrCapturedQuadrantEquals(move, quadrant) : false);
}

double Node::getUCT() {
    if (oldUCT){
        if (parent && numVisits != 0) {
            UCT = numWins / (double)numVisits + sqrt(2 * log(parent->numVisits) / numVisits);
        }
        else{
            UCT = 100;
        }
        oldUCT = false;
    }
    return UCT;
}
unsigned int Node::getNumWins() { return numWins; }
unsigned int Node::getNumVisits() { return numVisits; }
void Node::incrementWins(const int& i) { 
    numWins += i;
    oldUCT = true;
}
void Node::incrementVisits(const int& i) { 
    numVisits += i;
    oldUCT = true;
}

s_int Node::getLength() { return length; }

void Node::merge(const Node& node) {
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
}

s_int Node::getPlayer() { return length%2 == 0 ? P2 : P1; }
Node* Node::getParent() { return parent; }
void Node::setNumChildren(unsigned int num) {
    children.clear();
    children.reserve(num);
}
bool Node::hasNoChildren() { return children.empty(); }
vector<pair<unique_ptr<Move>, unique_ptr<Node>>>& Node::getChildren() { return children; }
unique_ptr<Node>& Node::getChild(const int& i) {
    if (children[i].second == nullptr){
        children[i].second = make_unique<Node>(children[i].first.get(), this, false);
    }
    return children[i].second;
}
unique_ptr<Node>& Node::back() {
    if (children.back().second == nullptr){
        children.back().second = make_unique<Node>(children.back().first.get(), this, false);
    }
    return children.back().second;
}
void Node::addChild(unique_ptr<Move>& move, unique_ptr<Node>& node) {
    // unique_ptr<Move> move = make_unique<Move>(node->move.get());
    Child child {std::move(move), std::move(node)};
    children.emplace_back(std::move(child));
}
void Node::addChild(unique_ptr<Move>& move) {
    // unique_ptr<Move> move = make_unique<Move>(node->move.get());
    Child child {std::move(move), nullptr};
    children.emplace_back(std::move(child));
}
void Node::setChild(const Move& move) {
    for (auto& child : children) {
        if (child.first->first == move.first && child.first->second == move.second) {
            Move* move = child.first.get();
            Node* moveChild = child.second.get();
            child.first.release();
            child.second.release();
            children.clear();
            unique_ptr<Move> selectedMove {move};
            unique_ptr<Node> selectedChild {moveChild};
            addChild(selectedMove, selectedChild);
            return;
        }
    }
    if (isLegal(move)) {
        children.clear();
        unique_ptr<Move> newMove = make_unique<Move>(move);
        addChild(newMove);
        back();
        return;
    }
    ostringstream err;
    err << "Could not find child with move:  " << move.first << " " << move.second;
    throw err.str();
}

void Node::buildQuadrant(Quadrant& array) {
    Node* current = this;
    do {
        if (current->capturedQuadrant != N) {
            array[current->move->first] = current->capturedQuadrant;
        }
        current = current->parent;
    } while (current != nullptr);
}
void Node::buildQuadrant(Quadrant& array, const int& quadrant) {
    Node* current = this;
    s_int player = length%2 == 0 ? P2 : P1;
    do {
        if (current->move && current->move->first == quadrant) {
            array[current->move->second] = player;
        }
        current = current->parent;
        player = player == P2 ? P1 : P2;
    } while (current != nullptr);
}
void Node::buildBoard2D(Board2D& array) {
    Node* current = this;
    s_int player = length%2 == 0 ? P2 : P1;
    do {
        if (current->move) {
            array[current->move->first][current->move->second] = player;
        }
        current = current->parent;
        player = player == P2 ? P1 : P2;
    } while (current);
}

std::ostream& Node::printTrace(std::ostream& out) {
    if (parent) {
        parent->printTrace(out);
    }
    if (move) {
        out << move->first << move->second;
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