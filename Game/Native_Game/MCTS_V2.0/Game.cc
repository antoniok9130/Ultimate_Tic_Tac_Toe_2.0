//
// Created by Antonio on 2018-04-18.
//
#include "Game.h"
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <list>
#include <utility>
#include "Node.h"

using namespace std;

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
    array<vector<int>, 9> remainingBoard;
    for (int i = 0; i < 9; ++i) {
        getRemaining(board[i], remainingBoard[i]);
    }

    Quadrant quadrants = make_Quadrant();
    node->buildQuadrant(quadrants);
    vector<int> remainingQuadrants;
    getRemaining(quadrants, remainingQuadrants);

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
            moveGlobal = getRandomRemaining(remainingQuadrants);
        }
        moveLocal = getRandomRemaining(remainingBoard[moveGlobal]);

        player = player == P2 ? P1 : P2;
        board[moveGlobal][moveLocal] = player;
        removeFromRemaining(remainingBoard[moveGlobal], moveLocal);

        quadrants[moveGlobal] = check3InRow(board[moveGlobal]);
        if (quadrants[moveGlobal] != N) {
            removeFromRemaining(remainingQuadrants, moveGlobal);
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