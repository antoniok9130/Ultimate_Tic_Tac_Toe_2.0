#include "UTTT_MCTS.h"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <sstream>

using namespace std;

///////////////////////////////////////////////////////////////
////////////////////////// Board.cc ///////////////////////////
///////////////////////////////////////////////////////////////

Move::Move(int first, int second) : first{first}, second{second} {}
Move::Move(const Move& other) : first{other.first}, second{other.second} {}
Move::Move(Move&& other) : first{std::move(other.first)}, second{std::move(other.second)} {}
Move& Move::operator=(const Move& other) {
    first = other.first;
    second = other.second;
    return *this;
}
Move& Move::operator=(Move&& other) {
    first = std::move(other.first);
    second = std::move(other.second);
    return *this;
}

string getBoardSymbol(const int& value, bool simple) {
    return value == P1 ? "X" : (value == P2 ? "O" : (simple ? "_" : " "));
}

int triple0[2][2] = {{1, 2}, {3, 6}};
int triple4[4][2] = {{3, 5}, {1, 7}, {0, 8}, {2, 6}};
int triple8[2][2] = {{6, 7}, {2, 5}};

int check3InRow(const Quadrant& quadrant) {
    bool checkTie = true;
    if (quadrant[0] != N) {
        for (const auto& t : triple0) {
            if (quadrant[0] == quadrant[t[0]] && quadrant[t[0]] == quadrant[t[1]]) {
                return quadrant[0];
            }
        }
    } else {
        checkTie = false;
    }
    if (quadrant[4] != N) {
        for (const auto& t : triple4) {
            if (quadrant[4] == quadrant[t[0]] && quadrant[t[0]] == quadrant[t[1]]) {
                return quadrant[4];
            }
        }
    } else {
        checkTie = false;
    }
    if (quadrant[8] != N) {
        for (const auto& t : triple8) {
            if (quadrant[8] == quadrant[t[0]] && quadrant[t[0]] == quadrant[t[1]]) {
                return quadrant[8];
            }
        }
    } else {
        checkTie = false;
    }
    return (checkTie && quadrant[1] != N && quadrant[2] != N && quadrant[3] != N && quadrant[5] != N &&
            quadrant[6] != N && quadrant[7] != N)
               ? TIE
               : N;
}

int g_seed = time(NULL);
inline int fastrand() {
    g_seed = (214013 * g_seed + 2531011);
    return (g_seed >> 16) & 0x7FFF;
}
int getRandomRemaining(Quadrant& quadrant) {
    int r = 0;
    do {
        r = fastrand() % 9;
    } while (quadrant[r] != N);
    return r;
}

Quadrant make_Quadrant() {
    Quadrant quadrant;
    for (auto& e : quadrant) {
        e = 0;
    }
    return quadrant;
}
Board2D make_Board2D() {
    Board2D board;
    for (auto& quadrant : board) {
        for (auto& e : quadrant) {
            e = 0;
        }
    }
    return board;
}
ostream& operator<<(ostream& out, Quadrant& quadrant) {
    for (int c = 0; c < 3; ++c) {
        for (int d = 0; d < 3; ++d) {
            out << getBoardSymbol(quadrant[3 * c + d]);
        }
        out << endl;
    }
    return out;
}
ostream& operator<<(ostream& out, Board2D& board) {
    for (int a = 0; a < 3; ++a) {
        for (int b = 0; b < 3; ++b) {
            for (int c = 0; c < 3; ++c) {
                for (int d = 0; d < 3; ++d) {
                    out << getBoardSymbol(board[3 * a + c][3 * b + d]);
                }
                out << "  ";
            }
            out << endl;
        }
        out << endl;
    }
    return out;
}

const char* verticalSpace = "     │   │    ║    │   │    ║    │   │    ";
const char* verticalDivide = "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ";
const char* bigVerticalDivide = " ═════════════╬═════════════╬═════════════";

// const std::vector<std::string> fancyBoard = {
// "     │   │    ║    │   │    ║    │   │    ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "     │   │    ║    │   │    ║    │   │    ",
// " ═════════════╬═════════════╬═════════════",
// "     │   │    ║    │   │    ║    │   │    ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "     │   │    ║    │   │    ║    │   │    ",
// " ═════════════╬═════════════╬═════════════",
// "     │   │    ║    │   │    ║    │   │    ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ",
// "   x │ x │ x  ║  x │ x │ x  ║  x │ x │ x  ",
// "     │   │    ║    │   │    ║    │   │    "
// };
ostream& print(ostream& out, Board2D& board, Quadrant& quadrant, bool simple) {
    if (simple) {
        for (int a = 0; a < 3; ++a) {
            for (int b = 0; b < 3; ++b) {
                for (int c = 0; c < 3; ++c) {
                    for (int d = 0; d < 3; ++d) {
                        out << getBoardSymbol(board[3 * a + c][3 * b + d], simple);
                    }
                    out << "  ";
                }
                if (a == 0) {
                    out << "   ";
                    for (int d = 0; d < 3; ++d) {
                        out << getBoardSymbol(quadrant[3 * b + d], simple);
                    }
                }
                out << endl;
            }
            out << endl;
        }
    } else {
        out << endl;
        for (int a = 0; a < 3; ++a) {
            if (a != 0) {
                out << bigVerticalDivide << endl;
            }
            out << verticalSpace << endl;
            for (int b = 0; b < 3; ++b) {
                if (b != 0) {
                    out << verticalDivide << endl;
                }
                out << "  ";
                for (int c = 0; c < 3; ++c) {
                    if (c != 0) {
                        out << " ║ ";
                    }
                    for (int d = 0; d < 3; ++d) {
                        if (d != 0) {
                            out << "│";
                        }
                        out << " " << getBoardSymbol(board[3 * a + c][3 * b + d], simple) << " ";
                    }
                    // out << "  ";
                }
                out << " " << endl;
            }
            out << verticalSpace << endl;
        }
        out << endl;
    }
    return out;
}

///////////////////////////////////////////////////////////////
////////////////////////// Node.cc ////////////////////////////
///////////////////////////////////////////////////////////////

Node::Node() {}

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
        if (this->move && !capturedQuadrantEquals(this->move->second, true)) {
            nextQuadrant = this->move->second;
        }
        if (initialize) {
            if (this->winner == N) {
                init();
            } else {
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
}

bool Node::hasMove() { return move ? true : false; }
unique_ptr<Move>& Node::getMove() { return move; }
void Node::setMove(unique_ptr<Move>& move) {
    if (this->move == nullptr) {
        this->move = std::move(move);
        setMove();
    }
}
void Node::setMove() {
    if (move && !moveSet) {
        Quadrant currentQuadrant = make_Quadrant();
        buildQuadrant(currentQuadrant, move->first);
        capturedQuadrant = check3InRow(currentQuadrant);
        if (capturedQuadrant != N) {
            Quadrant allQuadrants = make_Quadrant();
            buildQuadrant(allQuadrants);
            winner = check3InRow(allQuadrants);
        }
        moveSet = true;
    }
}

int Node::getGlobal() { return move ? move->first : -1; }
int Node::getLocal() { return move ? move->second : -1; }
int Node::getWinner() { return winner; }
int Node::getNextQuadrant() { return nextQuadrant; }
int Node::getCapturedQuadrant() { return capturedQuadrant; }

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

double Node::getUCT() { return UCT; }
int Node::getNumWins() { return numWins; }
int Node::getNumVisits() { return numVisits; }
void Node::incrementWins(const int& i) { numWins += i; }
void Node::incrementVisits(const int& i) { numVisits += i; }

int Node::getLength() { return length; }

void Node::merge(const Node& node) {}

int Node::getPlayer() { return player; }
Node* Node::getParent() { return parent; }
void Node::setNumChildren(unsigned int num) {
    children.clear();
    children.reserve(num);
}
vector<unique_ptr<Node>>& Node::getChildren() { return children; }
void Node::addChild(unique_ptr<Node>& move) { children.emplace_back(std::move(move)); }
void Node::setChild(const Move& move) {
    for (auto& child : children) {
        if (child->move->first == move.first && child->move->second == move.second) {
            Node* moveChild = child.get();
            child.release();
            children.clear();
            children.emplace_back(unique_ptr<Node>(moveChild));
            return;
        }
    }
    ostringstream err;
    err << "Could not find child with move:  " << move.first << " " << move.second;
    throw err.str();
}

void Node::buildQuadrant(Quadrant& array) {
    if (capturedQuadrant != N) {
        array[move->first] = capturedQuadrant;
    }
    if (parent) {
        parent->buildQuadrant(array);
    }
}
void Node::buildQuadrant(Quadrant& array, const int& quadrant) {
    Node* current = this;
    do {
        if (current->move && current->move->first == quadrant) {
            array[current->move->second] = current->player;
        }
        current = current->parent;
    } while (current != nullptr);
}
void Node::buildBoard2D(Board2D& array) {
    Node* current = this;
    do {
        if (current->move) {
            array[current->move->first][current->move->second] = current->player;
        }
        current = current->parent;
    } while (current != nullptr);
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

Node* Node_new() { return new Node(); }
void Node_delete(Node* node) { delete node; }
int Node_getWinner(Node* node) { return node->getWinner(); }
int Node_getNumWins(Node* node) { return node->getNumWins(); }
int Node_getNumVisits(Node* node) { return node->getNumVisits(); }
Node* Node_setMove(Node* node, int first, int second) {
    Move move{first, second};
    node->setChild(move);
    return node->getChildren().back().get();
}

///////////////////////////////////////////////////////////////
////////////////////////// Game.cc ////////////////////////////
///////////////////////////////////////////////////////////////

Move getMove(Node* node, double duration) {
    auto start = chrono::system_clock::now();
    auto end = chrono::system_clock::now();
    std::chrono::duration<double> diff = end - start;
    while (diff.count() < duration) {
        for (int i = 0; i < 100; ++i) {
            select(node);
        }
        end = chrono::system_clock::now();
        diff = end - start;
    }
    if (node->getNumVisits() == 0) {
        throw "No Move found...";
    }
    return getChildVisitedMost(node);
}

Move getChildVisitedMost(Node* node) {
    int mostVisits = 0;
    vector<size_t> mostVisitedChildren;
    mostVisitedChildren.reserve(node->getChildren().size());
    size_t i = 0;
    for (auto& child : node->getChildren()) {
        if (child->getNumVisits() >= mostVisits) {
            if (child->getNumVisits() > mostVisits) {
                mostVisits = child->getNumVisits();
                mostVisitedChildren.clear();
            }
            mostVisitedChildren.emplace_back(i);
        }
        ++i;
    }
    if (mostVisitedChildren.size() == 0) {
        throw "mostVisitedChildren.size() == 0";
    }
    int r = mostVisitedChildren[rand() % mostVisitedChildren.size()];
    return Move{node->getChildren()[r]->getGlobal(), node->getChildren()[r]->getLocal()};
}
unique_ptr<Node>& getChildHighestUCT(Node* node) {
    double highestUCT = 0;
    vector<size_t> highestUCTChildren;
    highestUCTChildren.reserve(node->getChildren().size());
    size_t i = 0;
    for (auto& child : node->getChildren()) {
        if (child->getUCT() >= highestUCT) {
            if (child->getUCT() > highestUCT) {
                highestUCT = child->getUCT();
                highestUCTChildren.clear();
            }
            highestUCTChildren.emplace_back(i);
        }
        ++i;
    }
    if (highestUCTChildren.size() == 0) {
        throw "highestUCTChildren.size() == 0";
    }
    return node->getChildren()[highestUCTChildren[rand() % highestUCTChildren.size()]];
}

void select(Node* node) {
    // cout << "Selecting..." << endl;
    if (node->getChildren().empty()) {
        node->init();
        if (node->getWinner() != N) {
            backpropogate(node, node->getWinner());
        } else if (node->hasMove() && node->getNumVisits() == 0) {
            int winner = runSimulation(node);
            backpropogate(node, winner);
        } else {
            // cout << "Expanding	..." << endl;
            expand(node);
            // cout << "Expanded" << endl;
        }
    } else {
        select(getChildHighestUCT(node).get());
    }
}
void expand(Node* node) {
    if (node->getChildren().empty()) {
        list<Move> legalMoves;
        Quadrant allQuadrants = make_Quadrant();
        node->buildQuadrant(allQuadrants);
        if (node->hasMove() && allQuadrants[node->getLocal()] == N) {
            Quadrant nextQuadrant = make_Quadrant();
            node->buildQuadrant(nextQuadrant, node->getLocal());
            for (int i = 0; i < 9; ++i) {
                if (nextQuadrant[i] == 0) {
                    int local = i;
                    legalMoves.emplace_back(Move{node->getLocal(), local});
                }
            }
        } else {
            Board2D board = make_Board2D();
            node->buildBoard2D(board);
            for (int i = 0; i < 9; ++i) {
                if (allQuadrants[i] == N) {
                    for (int j = 0; j < 9; ++j) {
                        if (board[i][j] == 0) {
                            legalMoves.emplace_back(Move{i, j});
                        }
                    }
                }
            }
        }

        if (legalMoves.size() > 0) {
            node->setNumChildren(legalMoves.size());
            for (auto& legalMove : legalMoves) {
                auto child = make_unique<Node>(legalMove.first, legalMove.second, node, true);
                node->addChild(child);
            }
            if (node->getChildren().size() == 0) {
                throw "No Children...";
            }
            int random = rand() % node->getChildren().size();
            // cout << "Running Simulation" << endl;
            int winner = runSimulation(node->getChildren()[random].get());
            backpropogate(node->getChildren()[random].get(), winner);
            // cout << "Simulation ended and values updated" << endl;
        }
    }
}

int runSimulation(Node* node) {
    node->init();
    Board2D board = make_Board2D();
    node->buildBoard2D(board);

    Quadrant quadrants = make_Quadrant();
    node->buildQuadrant(quadrants);

    int moveGlobal = -1, moveLocal = -1;
    if (node->hasMove()) {
        moveGlobal = node->getGlobal();
        moveLocal = node->getLocal();
    }
    int player = node->getPlayer();
    int winner = node->getWinner();
    while (winner == N) {
        if (moveLocal != -1 && quadrants[moveLocal] == N) {
            moveGlobal = moveLocal;
        } else {
            moveGlobal = getRandomRemaining(quadrants);
        }
        moveLocal = getRandomRemaining(board[moveGlobal]);

        player = player == P2 ? P1 : P2;
        board[moveGlobal][moveLocal] = player;

        quadrants[moveGlobal] = check3InRow(board[moveGlobal]);
        if (quadrants[moveGlobal] != N) {
            winner = check3InRow(quadrants);
        }
    }
    return winner;
}

void backpropogate(Node* node, int winner) {
    if (node->getPlayer() == winner) {
        node->incrementWins();
    }
    node->incrementVisits();

    if (node->getParent()) {
        backpropogate(node->getParent(), winner);
    }

    node->updateUCT();
}

void MCTS_select(Node* node) { select(node); }
void MCTS_expand(Node* node) { expand(node); }
int MCTS_runSimulation(Node* node) { return runSimulation(node); }
void MCTS_backpropogate(Node* node, int winner) { backpropogate(node, winner); }
