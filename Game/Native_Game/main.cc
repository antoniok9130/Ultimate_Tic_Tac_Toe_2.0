#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <utility>
#include "MCTS/Game.h"
#include "MCTS/Node.h"

using namespace std;

void play() {
    Node* game = new Node();
    string s;
    try {
        while (game->getWinner() == N) {
            Board2D board = make_Board2D();
            game->buildBoard2D(board);
            cout << board;
            cout << "Enter Move:   ";
            if (!getline(cin, s)) break;
            istringstream iss{s};
            int global, local;
            if (iss >> global) {
                if (!(iss >> local)) {
                    Quadrant allQuadrants;
                    game->buildQuadrant(allQuadrants);

                    if (game->hasMove() && allQuadrants[game->getLocal()] == N) {
                        local = global;
                        global = game->getLocal();
                    } else {
                        continue;
                    }
                }
                const Move move = Move{std::move(global), std::move(local)};
                if (game->isLegal(move)) {
                    unique_ptr<Node> nextState = make_unique<Node>(move, game);
                    game->addChild(nextState);
                    game = game->getChildren().back().get();

                    Board2D nextBoard = make_Board2D();
                    game->buildBoard2D(nextBoard);
                    cout << nextBoard;
                    if (game->getWinner() == N) {
                        unique_ptr<Node>& moveNode = getMove(game);
                        cout << "G:  " << moveNode->getGlobal() << "     L:  " << moveNode->getLocal() << endl;
                        cout << "W:  " << moveNode->getNumWins() << "     V:  " << moveNode->getNumVisits() << endl;
                        game = moveNode.get();
                    }
                } else {
                    cout << "Not Valid Move:  " << move.first << " " << move.second << endl;
                }
            } else {
                break;
            }
        }
        Board2D board = make_Board2D();
        game->buildBoard2D(board);
        cout << board;
        cout << "Winner:  " << game->getWinner();
    } catch (string s) {
        cout << s << endl;
    } catch (const char* s) {
        cout << s << endl;
    }
    delete game;
}

int main() {
    play();
    return 0;
}