
// #include <condition_variable>
#include <fstream>
#include <iostream>
#include <memory>
// #include <mutex>
#include <sstream>
#include <string>
// #include <thread>
#include <utility>
#include "Game.h"
#include "Node.h"

using namespace std;

// std::mutex m;
// std::condition_variable cv;
Node* game = nullptr;
// bool playInBackground = false;

// void backgroundPlay(Node* game, bool& continuePlaying) {
//     select(game);
//     size_t numTimesPlayed = 0;
//     while (continuePlaying) {
//         for (auto& child : game->getChildren()) {
//             select(child.get());
//         }
//         ++numTimesPlayed;
//     }
//     cout << "Played " << numTimesPlayed << " iterations in the background" << endl;
// }

void selfPlay() {
    game = new Node();
    try {
        select(game);
        game->setChild(Move{rand() % 9, rand() % 9});
        game = game->getChildren().back().get();
        while (game->getWinner() == N) {
            // Board2D board = make_Board2D();
            // game->buildBoard2D(board);
            // cout << board;
            // cout << "Getting Move" << endl;
            Move move = getMove(game, 3.5);
            // cout << "Search Space Size:  " << game->getNumVisits() << endl;
            // cout << "G:  " << move.first << "     L:  " << move.second << endl;
            game->setChild(move);
            game = game->getChildren().back().get();
            // cout << "W:  " << game->getNumWins() << "     V:  " << game->getNumVisits() << endl;
        }
        cout << "Winner:  " << game->getWinner() << endl;
        Board2D board = make_Board2D();
        game->buildBoard2D(board);
        cout << board;
        game->printTrace(cout) << endl;

        std::ofstream outfile;
        outfile.open("RecordedGames.txt", std::ios_base::app);
        game->printTrace(outfile) << endl;

    } catch (...) {
        cerr << "Failed to complete game" << endl;
    }
    delete game;
}

void play() {
    game = new Node();
    select(game);
    string s;
    try {
        double thinkingTime = 3.0;
        cout << "Enter thinking time (in seconds):  ";
        if (getline(cin, s)) {
            istringstream thinkingss{s};
            thinkingss >> thinkingTime;
        }
        // bool continuePlaying = true;
        // thread bplay(backgroundPlay, game, continuePlaying);

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
                    if (game->getNextQuadrant() == -1) {
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
                    game->setChild(move);
                    game = game->getChildren().back().get();

                    Board2D nextBoard = make_Board2D();
                    game->buildBoard2D(nextBoard);
                    cout << nextBoard;
                    if (game->getWinner() == N) {
                        // continuePlaying = false;
                        // bplay.join();

                        cout << "Getting Move" << endl;
                        move = getMove(game, thinkingTime);
                        cout << "Search Space Size:  " << game->getNumVisits() << endl;
                        cout << "G:  " << move.first << "     L:  " << move.second << endl;
                        game->setChild(move);
                        game = game->getChildren().back().get();
                        cout << "W:  " << game->getNumWins() << "     V:  " << game->getNumVisits() << endl;
                        // continuePlaying = true;
                        // bplay = thread(backgroundPlay, game, continuePlaying);
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
    srand(time(NULL));
    play();
    // for (int i = 0; i < 20; ++i) {
    //     selfPlay();
    // }
    return 0;
}