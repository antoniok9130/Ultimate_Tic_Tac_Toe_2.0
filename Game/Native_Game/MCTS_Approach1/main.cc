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
            Board2D board = make_Board2D();
            game->buildBoard2D(board);
            cout << board;
            cout << "Enter Move:   ";
            if (!getline(cin, s)) break;
            istringstream iss{s};
            int global, local;
            if (iss >> global) {
                Move move{-1, -1};
                if (!(iss >> local)) {
					if (game->getNextQuadrant() == -1){
						cout << "Need a global input" << endl;
						continue;
					}
                    local = global;
                    global = game->getLocal();
                    move = Move{std::move(global), std::move(local)};
                } else {
                    move = Move{std::move(global), std::move(local)};
                }
                if (move.first >= 0 && move.first <= 8 && move.second >= 0 && move.second <= 8 && game->isLegal(move)) {
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
                cout << "Please Enter move in quadrant:  " << game->getNextQuadrant() << endl;
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