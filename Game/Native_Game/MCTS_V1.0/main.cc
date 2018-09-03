#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <utility>
#include "Game.h"
#include "Node.h"

using namespace std;

void play() {
    Node* game = new Node();
    string s;
    try {
        while (game->getWinner() == N) {
            game->buildBoard2D();
            cout << game->getBoard();
            cout << "Enter Move:   ";
            if (!getline(cin, s)) break;
            istringstream iss{s};
            int global, local;
            if (iss >> global) {
                if (!(iss >> local)) {
                    game->buildQuadrant();
                    if (game->hasMove() && game->getQuadrants()[game->getLocal()] == N) {
                        local = global;
                        global = game->getLocal();
                    } else {
                        continue;
                    }
                }
                const Move move = Move{std::move(global), std::move(local)};
                if (game->isLegal(move)) {
                    unique_ptr<Node> nextState = make_unique<Node>(move, game);
                    game->setChild(nextState);
                    game = game->getChildren().back().get();

                    game->buildBoard2D();
                    cout << game->getBoard();
                    if (game->getWinner() == N) {
                        unique_ptr<Node> moveNode{std::move(getMove(game))};
                        cout << "G:  " << moveNode->getGlobal() << "     L:  " << moveNode->getLocal() << endl;
                        cout << "W:  " << moveNode->getNumWins() << "     V:  " << moveNode->getNumVisits() << endl;
                        game->setChild(moveNode);
                        game = game->getChildren().back().get();
                    }
                } else {
                    cout << "Not Valid Move:  " << move.first << " " << move.second << endl;
                }
            }
        }
        game->buildBoard2D();
        cout << game->getBoard();
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