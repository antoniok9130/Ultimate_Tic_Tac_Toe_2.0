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

Move getMove(Node* node, int iterations) {
    int* move = isWin(node);
    if (move) {
        cout << "Instant Win!" << endl;
        Move winningMove {move[0], move[1]};
        free(move);
        return winningMove;
    }

    for (int i = 0; i < iterations; ++i) {
        select(node);
    }
    if (node->getNumVisits() == 0) {
        throw "No Move found...";
    }
    return getChildVisitedMost(node);
}
// Move getMove(Node* node, double duration) {
//     int* move = isWin(node);
//     if (move) {
//         return Move{move[0], move[1]};
//     }

//     auto start = chrono::system_clock::now();
//     auto end = chrono::system_clock::now();
//     std::chrono::duration<double> diff = end - start;
//     while (diff.count() < duration) {
//         for (int i = 0; i < 100; ++i) {
//             select(node);
//         }
//         end = chrono::system_clock::now();
//         diff = end - start;
//     }
//     if (node->getNumVisits() == 0) {
//         throw "No Move found...";
//     }
//     return getChildVisitedMost(node);
// }

int* isWin(Node* node) {
    int AIPlayer = node->getPlayer() == P1 ? P2 : P1;
    Quadrant quadrants = make_Quadrant();
    node->buildQuadrant(quadrants);
    if (node->getNextQuadrant() != -1) {
        if (potential3inRow(quadrants, node->getNextQuadrant(), AIPlayer)) {
            Quadrant quadrant = make_Quadrant();
            node->buildQuadrant(quadrant, node->getNextQuadrant());
            for (int i = 0; i < 9; ++i) {
                if (quadrant[i] == N && potential3inRow(quadrant, i, AIPlayer)) {
                    int* move = new int[2];
                    move[0] = node->getNextQuadrant();
                    move[1] = i;
                    return move;
                }
            }
        }
    } else {
        for (int i = 0; i < 9; ++i) {
            if (quadrants[i] == N && potential3inRow(quadrants, i, AIPlayer)) {
                Quadrant quadrant = make_Quadrant();
                node->buildQuadrant(quadrant, i);
                for (int j = 0; j < 9; ++j) {
                    if (quadrant[j] == N && potential3inRow(quadrant, j, AIPlayer)) {
                        int* move = new int[2];
                        move[0] = i;
                        move[1] = j;
                        return move;
                    }
                }
            }
        }
    }
    return nullptr;
}

int g_seed = time(NULL);
inline int fastrand() {
    g_seed = (214013 * g_seed + 2531011);
    return (g_seed >> 16) & 0x7FFF;
}

Move getChildVisitedMost(Node* node) {
    unsigned int mostVisits = 0;
    int childIndex = -1;
    int i = 0;
    for (auto& child : node->getChildren()) {
        unsigned int numVisits = child.second ? child.second->getNumVisits() : 0;
        if ((numVisits > mostVisits) || (numVisits == mostVisits && (fastrand() % 2 == 1))) {
            mostVisits = numVisits;
            childIndex = i;
        }
        ++i;
    }
    auto& child = node->getChild(childIndex);
    return Move{child->getGlobal(), child->getLocal()};
}
Node* getChildHighestUCT(Node* node) {
    double highestUCT = 0;
    int childIndex = -1;
    int i = 0;
    for (auto& child : node->getChildren()) {
        double uct = child.second ? child.second->getUCT() : 100;
        if ((uct > highestUCT) || (uct == highestUCT && (fastrand() % 2 == 1))) {
            highestUCT = uct;
            childIndex = i;
        }
        ++i;
    }
    // cout << "Highest UCT:  " << highestUCT << endl;
    return node->getChild(childIndex).get();
}

void select(Node* node) {
    // cout << "Selecting..." << endl;
    if (node->hasNoChildren()) {
        // cout << "Node " << node << " has no children" << endl;
        node->init();
        if (node->getWinner() != N) {
            // cout << "Backpropogating 1 ..." << endl;
            backpropogate(node, node->getWinner());
        } else if (node->hasMove() && node->getNumVisits() == 0) {
            // cout << "Backpropogating 2 ..." << endl;
            int winner = runSimulation(node);
            backpropogate(node, winner);
        } else {
            // cout << "Expanding..." << endl;
            expand(node);
            // cout << "Expanded" << endl;
        }
    } else {
        select(getChildHighestUCT(node));
    }
    // cout << "Selected" << endl;
}
void expand(Node* node) {
    if (node->hasNoChildren()) {
        list<unique_ptr<Move>> legalMoves;
        Quadrant allQuadrants = make_Quadrant();
        node->buildQuadrant(allQuadrants);
        if (node->hasMove() && allQuadrants[node->getLocal()] == N) {
            Quadrant nextQuadrant = make_Quadrant();
            node->buildQuadrant(nextQuadrant, node->getLocal());
            for (int i = 0; i < 9; ++i) {
                if (nextQuadrant[i] == N) {
                    legalMoves.emplace_back(make_unique<Move>(node->getLocal(), i));
                }
            }
        } else {
            Board2D board = make_Board2D();
            node->buildBoard2D(board);
            for (int i = 0; i < 9; ++i) {
                if (allQuadrants[i] == N) {
                    for (int j = 0; j < 9; ++j) {
                        if (board[i][j] == 0) {
                            legalMoves.emplace_back(make_unique<Move>(i, j));
                        }
                    }
                }
            }
        }

        if (legalMoves.size() > 0) {
            for (auto& legalMove : legalMoves) {
                node->addChild(legalMove);
            }
            legalMoves.clear();
            if (node->getChildren().size() == 0) {
                throw "No Children...";
            }
            int random = rand() % node->getChildren().size();
            // cout << "Running Simulation..." << endl << std::flush;
            int winner = runSimulation(node->getChild(random).get());
            // cout << "Backpropogating 3..." << endl << std::flush;
            backpropogate(node->getChild(random).get(), winner);
            // cout << "Simulation ended and values updated" << endl << std::flush;
        }
    }
}

int runSimulation(Node* node) {
    node->init();
    Board2D board = make_Board2D();
    node->buildBoard2D(board);
    Quadrant quadrants = make_Quadrant();
    node->buildQuadrant(quadrants);

    int numRemainingQuadrants = 0;
    auto numRemainingBoard = array<int, 9>();
    auto potentialQuadrants = array<int, 9>();
    for (int i = 0; i < 9; ++i) {
        if (quadrants[i] == N) {
            ++numRemainingQuadrants;
            potentialQuadrants[i] = potential3inRow(quadrants, i);
            for (int j = 0; j < 9; ++j) {
                if (board[i][j] == N) {
                    ++numRemainingBoard[i];
                }
            }
        }
    }

    int moveGlobal = -1, moveLocal = -1;
    if (node->hasMove()) {
        moveGlobal = node->getGlobal();
        moveLocal = node->getLocal();
    }
    int player = node->getPlayer();
    int winner = node->getWinner();
    // int length = node->getLength();
    while (winner == N) {
        if (moveLocal != -1 && quadrants[moveLocal] == N) {
            moveGlobal = moveLocal;
        } else {
            moveGlobal = getRandomRemaining(quadrants);
        }

        if (potentialQuadrants[moveGlobal] == player || potentialQuadrants[moveGlobal] == B) {
            for (int i = 0; i < 9; ++i) {
                if (board[moveGlobal][i] == N && potential3inRow(board[moveGlobal], i, player)) {
                    return player;
                }
            }
        }

        moveLocal = getRandomRemaining(board[moveGlobal]);
        player = player == P2 ? P1 : P2;
        board[moveGlobal][moveLocal] = player;
        --numRemainingBoard[moveGlobal];
        // ++length;

        if (check3InRow(board[moveGlobal], moveLocal)) {
            quadrants[moveGlobal] = player;
            --numRemainingQuadrants;

            updatePotential3inRow(potentialQuadrants, quadrants, moveGlobal);

            if (check3InRow(quadrants, moveGlobal)) {
                winner = player;
                return player;
            } else if (numRemainingQuadrants <= 0) {
                winner = TIE;
                return TIE;
            }
        } else if (numRemainingBoard[moveGlobal] <= 0) {
            quadrants[moveGlobal] = TIE;
            --numRemainingQuadrants;
            if (numRemainingQuadrants <= 0) {
                winner = TIE;
                return TIE;
            }
        }

        // if (length > 81){
        //     cerr << "Depth of simulation is too deep" << endl;
        //     throw "";
        // }
    }
    return winner;
}

void backpropogate(Node* node, int winner) {



    Node* current = node;
    // int depth = 0;
    do {
        current->incrementWins();
        current->incrementVisits();
        current = current->getParent();
        // ++depth;
        if (current){
            current->incrementVisits();
            current = current->getParent();
            ++depth;
        }
        // if (depth > 81){
        //     cerr << "Depth of backpropogation is too deep" << endl;
        //     throw "";
        // }
    } while (current != nullptr);

    // node->updateUCT();
}

// void MCTS_select(Node* node) { select(node); }
// void MCTS_expand(Node* node) { expand(node); }
// int MCTS_runSimulation(Node* node) { return runSimulation(node); }
// void MCTS_backpropogate(Node* node, int winner) { backpropogate(node, winner); }