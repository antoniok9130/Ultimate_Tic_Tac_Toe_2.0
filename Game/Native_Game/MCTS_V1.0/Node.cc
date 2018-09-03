//
// Created by Antonio on 2018-04-18.
//

#include "Node.h"
#include <cmath>
#include <iostream>
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

Node::Node(int moveGlobal, int moveLocal, Node* parent, bool initialize)
    : Node{Move{std::move(moveGlobal), std::move(moveLocal)}, parent, initialize} {}
Node::Node(const Move& move, Node* parent, bool initialize)
    : winner{parent ? parent->winner : N},
      player{parent ? (parent->player == P1 ? P2 : P1) : P1},
      length{parent ? (parent->length + 1) : 1},
      move{make_unique<Move>(std::move(move))},
      parent{parent},
      initialized{parent ? false : true} {
    if (parent) {
        if (initialize) {
            if (this->winner == N) {
                init();
            } else {
                // this->quadrants = make_unique<Quadrants>(parent->quadrants);
                // this->board = make_unique<Board2D>(parent->board);
                initialized = true;
            }
        }
    } else {
        if (this->move) {
            // board->set(move->first, move->second, P1);
        } else {
            player = N;
        }
        initialized = true;
    }
}

void Node::init() {
    if (!initialized) {
        if (move) {
            setMove();
        } else {
            move = make_unique<Move>(*parent->move);
        }
        initialized = true;
    }
}

void Node::updateUCT() {
    if (parent && numVisits != 0) {
        UCT = numWins / (double)numVisits + sqrt(2 * log(parent->numVisits) / numVisits);
    }
}

bool Node::isLegal(const Move& move) {
    return (nextQuadrant == -1 || move.first == nextQuadrant) && !moveOrCapturedQuadrantEquals(move, move.first);
    // quadrants->remainingContains(move->first) && (nextQuadrant == -1 || move->first == nextQuadrant) &&
    //     board->remainingContains(move);
}

bool Node::hasMove() { return move ? true : false; }
unique_ptr<Move>& Node::getMove() { return move; }
// void Node::setMove(int moveGlobal, int moveLocal) {
//     if (!this->move) {
//         this->move = make_unique<int, int>(std::move(moveGlobal), std::move(moveLocal));
//         setMove();
//     }
// }
void Node::setMove(unique_ptr<Move>& move) {
    if (this->move == nullptr) {
        this->move = std::move(move);
        setMove();
    }
}
void Node::setMove() {
    if (move && !moveSet) {
        buildBoard2D();
        int filled = check3InRow((*board)[move->first]);
        if (filled != N) {
            capturedQuadrant = T;
            buildQuadrant();
            winner = check3InRow(*quadrants);
        }
        moveSet = true;
    }
}

int Node::getGlobal() { return move ? move->first : -1; }
int Node::getLocal() { return move ? move->second : -1; }
int Node::getWinner() { return winner; }
int Node::getNextQuadrant() { return nextQuadrant; }
int Node::getCapturedQuadrant() { return capturedQuadrant; }

bool Node::moveEquals(const Move& move, bool backpropogate) {
    return (this->move && this->move->first == move.first && this->move->second == move.second) ||
           ((backpropogate && parent) ? parent->moveEquals(move, backpropogate) : false);
}
bool Node::capturedQuadrantEquals(const int& quadrant, bool backpropogate) {
    return (capturedQuadrant != N && capturedQuadrant != T && move && move->first == quadrant) ||
           ((backpropogate && parent) ? parent->capturedQuadrantEquals(quadrant, backpropogate) : false);
}
bool Node::moveOrCapturedQuadrantEquals(const Move& move, const int& quadrant) {
    return moveEquals(move) || capturedQuadrantEquals(quadrant) ||
           (parent ? parent->moveOrCapturedQuadrantEquals(move, quadrant) : false);
}

double Node::getUCT() { return UCT; }
int Node::getNumWins() { return numWins; }
int Node::getNumVisits() { return numVisits; }
void Node::incrementWins(const int& i) { numWins += i; }
void Node::incrementVisits(const int& i) { numVisits += i; }

int Node::getLength() { return length; }

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

int Node::getPlayer() { return player; }
Node* Node::getParent() { return parent; }
void Node::setNumChildren(unsigned int num) {
    children.clear();
    children.reserve(num);
}
vector<unique_ptr<Node>>& Node::getChildren() { return children; }
void Node::addChild(unique_ptr<Node>& move) { children.emplace_back(std::move(move)); }
void Node::setChild(unique_ptr<Node>& move) {
    children.clear();
    children.emplace_back(std::move(move));
}

void Node::buildQuadrant() {
    if (!quadrants) {
		quadrants = make_Quadrant();
        if (parent && parent->quadrants) {
            For(0, 9) { (*quadrants)[i] = (*parent->quadrants)[i]; }
        } else {
            Node* current = this;
            do {
                if (current->capturedQuadrant != N) {
                    (*quadrants)[current->move->first] = current->capturedQuadrant;
                }
                current = current->parent;
            } while (current != nullptr);
        }
    }
}
// void Node::buildQuadrant(Quadrant& array, const int& quadrant) {
//     Node* current = this;
//     do {
//         if (current->move && current->move->first == quadrant) {
//             array[current->move->second] = current->player;
//         }
//         current = current->parent;
//     } while (current != nullptr);
// }
void Node::buildBoard2D() {
    if (!board) {
		board = make_Board2D();
        if (parent && parent->board) {
            For(0, 9) {
                Forj(0, 9) { (*board)[i][j] = (*parent->board)[i][j]; }
            }
			if (move){
				(*board)[move->first][move->second] = player;
			}
        } else {
            Node* current = this;
            do {
                if (current->move) {
                    (*board)[current->move->first][current->move->second] = player;
                }
                current = current->parent;
            } while (current != nullptr);
        }
    }
}

Quadrant& Node::getQuadrants() { return *quadrants; }

Board2D& Node::getBoard() { return *board; }

// ostream& operator<<(ostream& out, Node& node) {
//     out << node.getQuadrants() << endl;
//     out << node.getBoard() << endl;
//     return out;
// }
