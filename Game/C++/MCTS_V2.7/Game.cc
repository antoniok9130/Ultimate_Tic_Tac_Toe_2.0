//
// Created by Antonio on 2018-04-18.
//
#include "Game.h"
#include "Board.h"
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <list>
#include <utility>
#include "Node.h"

using namespace std;

int numP1Wins = 0;
int numP2Wins = 0;
int numTies = 0;

unique_ptr<Move> getMove(Node* node) {
    unique_ptr<Move> move = isWin(node);
    if (move) {
        return move;
    }
    numP1Wins = 0;
    numP2Wins = 0;
    numTies = 0;

    size_t iteration = 0;
    while(NodePool::size() > 81) {
        select(node);
        ++iteration;
        if (iteration > NodePool::maxSize()){
            break;
        }
    }
    if (node->getNumVisits() == 0) {
        throw "No Move found...";
    }
    cout << "    numP1Wins:  " << numP1Wins << endl;
    cout << "    numP2Wins:  " << numP2Wins << endl;
    cout << "    numTies:    " << numTies << endl;
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

unique_ptr<Move> isWin(Node* node) {
    int AIPlayer = node->getPlayer() == P1 ? P2 : P1;
    Quadrant quadrants = make_Quadrant();
    node->buildQuadrant(quadrants);
    if (node->getNextQuadrant() != -1) {
        if (potential3inRow(quadrants, node->getNextQuadrant(), AIPlayer)) {
            Quadrant quadrant = make_Quadrant();
            node->buildQuadrant(quadrant, node->getNextQuadrant());
            for (int i = 0; i < 9; ++i) {
                if (quadrant[i] == N && potential3inRow(quadrant, i, AIPlayer)) {
                    return make_unique<Move>(node->getNextQuadrant(), i);
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
                        return make_unique<Move>(i, j);
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

std::unique_ptr<Move> getChildVisitedMost(Node* node) {
    int mostVisits = 0;
    double sum = 0;
    int childIndex = -1;
    int i = 0;
    for (auto& child : node->getChildren()) {
        sum += child->getNumWins();
        if ((child->getNumVisits() > mostVisits) || (child->getNumVisits() == mostVisits && (fastrand() % 2 == 1))) {
            mostVisits = child->getNumVisits();
            childIndex = i;
        }
        ++i;
    }
    cout << sum << endl;
    return node->getChild(childIndex)->getMove();
}
Node* getChildHighestUCT(Node* node) {
    double highestUCT = 0;
    int childIndex = -1;
    int i = 0;
    for (auto& child : node->getChildren()) {
        if ((child->getUCT() > highestUCT) || (child->getUCT() == highestUCT && (fastrand() % 2 == 1))) {
            highestUCT = child->getUCT();
            childIndex = i;
        }
        ++i;
    }
    return node->getChild(childIndex);
}

void select(Node* node) {
    // cout << "Selecting..." << endl;
    if (node->hasNoChildren()) {
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
        select(getChildHighestUCT(node));
    }
}
void expand(Node* node) {
    if (node->hasNoChildren()) {
        list<Move> legalMoves;
        Quadrant allQuadrants = make_Quadrant();
        node->buildQuadrant(allQuadrants);
        if (node->hasMove() && allQuadrants[node->getLocal()] == N) {
            Quadrant nextQuadrant = make_Quadrant();
            node->buildQuadrant(nextQuadrant, node->getLocal());
            for (int i = 0; i < 9; ++i) {
                if (nextQuadrant[i] == N) {
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

        if (legalMoves.size() <= NodePool::size()) {
            node->setNumChildren(legalMoves.size());
            for (auto& legalMove : legalMoves) {
                Node* child = NodePool::getNode();
                child->init(legalMove.first, legalMove.second, node, false);
                node->addChild(child);
            }
            if (node->getChildren().size() == 0) {
                throw "No Children...";
            }
            int random = rand() % node->getChildren().size();
            // cout << "Running Simulation" << endl;
            int winner = runSimulation(node->getChild(random));
            backpropogate(node->getChild(random), winner);
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
        player = other(player);
        board[moveGlobal][moveLocal] = player;
        --numRemainingBoard[moveGlobal];

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
    }
    return winner;
}

void backpropogate(Node* node, int winner) {

    Node* current = node;

    if (winner == TIE){
        numTies += 1;
    }
    else if (winner == P1){
        numP1Wins += 1;
    }
    else if (winner == P2){
        numP2Wins += 1;
    }

    if (winner == TIE){
        while (current){
            current->incrementVisits();
            current = current->getParent();
        }
    }
    else if (current->getPlayer() == winner){
        while (current){
            current->incrementWins();
            current->incrementVisits();
            current = current->getParent();
            if (current){
                current->incrementVisits();
                current = current->getParent();
            }
        }
    }
    else {
        while (current){
            current->incrementVisits();
            current = current->getParent();
            if (current){
                current->incrementWins();
                current->incrementVisits();
                current = current->getParent();
            }
        }
    }
    
}

// void MCTS_select(Node* node) { select(node); }
// void MCTS_expand(Node* node) { expand(node); }
// int MCTS_runSimulation(Node* node) { return runSimulation(node); }
// void MCTS_backpropogate(Node* node, int winner) { backpropogate(node, winner); }