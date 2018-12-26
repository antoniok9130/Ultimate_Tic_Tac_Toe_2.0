
// #include <condition_variable>
#include <fstream>
#include <iostream>
#include <memory>
// #include <mutex>
#include <array>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <sstream>
#include <string>
#include <thread>
#include <utility>
#include "Board.h"
#include "Game.h"
#include "Node.h"

using namespace std;

// std::mutex m;
// std::condition_variable cv;
// Node* game = nullptr;
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

void analyze() {
    string s;
    int gameNum = 0;
    while (getline(cin, s)) {
        Board2D board = make_Board2D();
        Quadrant quadrants = make_Quadrant();
        int player = P1;
        istringstream iss{s};
        char g, l;
        while (iss >> g && iss >> l) {
            if (g >= '0' && g <= '8' && l >= '0' && l <= '8') {
                board[g - '0'][l - '0'] = player;
                player = player == P1 ? P2 : P1;
            } else {
                break;
            }
        }
        For(0, 9) { quadrants[i] = check3InRow(board[i]); }
        int winner = check3InRow(quadrants);
        ++gameNum;
        cout << "Game " << gameNum << ":" << endl;
        print(cout, board, quadrants);
        cout << "Winner:  " << winner << endl;
    }
}

Node* AI_move(Node* node, int iterations, std::ostream& logout=cout) {  // double thinkingTime
    logout << "    Player " << (node->getPlayer() == P1 ? P2 : P1) << " getting move" << endl;
    clock_t start = clock();
    Move move = getMove(node, iterations - node->getNumVisits());  // thinkingTime
    clock_t end = clock();
    logout << "    Search Space Size:  " << node->getNumVisits() << endl;
    logout << "    G:  " << move.first << "     L:  " << move.second << endl;
    node->setChild(move);
    node = node->getChildren().back().get();
    logout << "    W:  " << node->getNumWins() << "    V:  " << node->getNumVisits() << endl;
    logout << "    Confidence:  " << (node->getNumWins() / (double)node->getNumVisits()) << endl;
    logout << "    Time:  " << (double(end-start)/CLOCKS_PER_SEC) << endl;
    logout << endl;
    return node;
}

void selfPlay(Node* game, std::ostream& logout, std::ostream& recordout) {
    // game = new Node();
    try {
        while (game->getWinner() == N) {
            // Board2D board = make_Board2D();
            // game->buildBoard2D(board);
            // Quadrant quadrants = make_Quadrant();
            // game->buildQuadrant(quadrants);
            // print(cout, board, quadrants);

            game = AI_move(game, 250000, logout);
        }
        logout << "    Winner:  " << game->getWinner() << endl;
        // Board2D board = make_Board2D();
        // game->buildBoard2D(board);
        // cout << board;
        // game->printTrace(cout) << endl;

        game->printTrace(recordout) << endl;

    } catch (...) {
        logout << "Failed to complete game" << endl;
    }
}


const int movePriorities[88][2] = {
    {4, 4}, {4, 4}, {4, 4}, {4, 4}, {4, 0}, {4, 0}, {4, 2}, {4, 2}, {4, 6}, {4, 6}, {4, 8}, {4, 8}, 
    {0, 0}, {0, 2}, {0, 6}, {0, 8}, {2, 0}, {2, 2}, {2, 6}, {2, 8}, {6, 0}, {6, 2}, {6, 6}, {6, 8}, {8, 0}, {8, 2}, {8, 6}, {8, 8}, 
    {4, 1}, {4, 3}, {4, 5}, {4, 7}, {1, 1}, {3, 3}, {5, 5}, {7, 7}, 
    {0, 1}, {0, 3}, {0, 5}, {0, 7}, {1, 0}, {1, 2}, {1, 3}, {1, 5}, {1, 6}, {1, 7}, {1, 8}, {2, 1}, {2, 3}, {2, 5}, {2, 7}, 
    {3, 0}, {3, 1}, {3, 2}, {3, 5}, {3, 6}, {3, 7}, {3, 8}, {5, 0}, {5, 1}, {5, 2}, {5, 3}, {5, 6}, {5, 7}, {5, 8}, 
    {6, 1}, {6, 3}, {6, 5}, {6, 7}, {7, 0}, {7, 1}, {7, 2}, {7, 3}, {7, 5}, {7, 6}, {7, 8}, 
    {8, 1}, {8, 3}, {8, 5}, {8, 7}, {0, 4}, {1, 4}, {2, 4}, {3, 4}, {5, 4}, {6, 4}, {7, 4}, {8, 4}
};

void iterateSelfPlay(const string& logPath, const string& recordPath) {
    
    std::ofstream logout;
    logout.open(logPath, std::ios_base::app);

    std::ofstream recordout;
    recordout.open(recordPath, std::ios_base::app);

    int iteration = 1;
    while(true){
	for (auto& move : movePriorities) {
            logout << "Iteration " << iteration << ":   " << move[0] << ", " << move[1] << endl;

            Node* node = new Node();
            Node* game = node;
            game->setChild(Move{move[0], move[1]});
            game = game->getChild(0).get();
            selfPlay(game, logout, recordout);
            delete node;

            ++iteration;
       }
   }
}

void play() {
    Node* node = new Node();
    Node* game = node;
    string s;
    try {
        int player = 1;
        // cout << "Play as Player 1 or 2:  ";
        // if (getline(cin, s)) {
        //     istringstream playerss{s};
        //     playerss >> player;
        // }
        // if (player != 1 && player != 2) {
        //     throw "Invalid Player Number:  " + player;
        // }
        double thinkingTime = 2000000;
        // cout << "Enter thinking time for AI (in seconds):  ";
        // if (getline(cin, s)) {
        //     istringstream thinkingss{s};
        //     thinkingss >> thinkingTime;
        // }
        // bool continuePlaying = true;
        // thread bplay(backgroundPlay, game, continuePlaying);

        if (player == 2) {
            game = AI_move(game, thinkingTime);
        }

        while (game->getWinner() == N) {
            Board2D board = make_Board2D();
            game->buildBoard2D(board);
            Quadrant quadrants = make_Quadrant();
            game->buildQuadrant(quadrants);
            print(cout, board, quadrants, false);

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
                    Quadrant nextQuadrants = make_Quadrant();
                    game->buildQuadrant(nextQuadrants);
                    print(cout, nextBoard, nextQuadrants, false);
                    if (game->getWinner() == N) {
                        // continuePlaying = false;
                        // bplay.join();

                        game = AI_move(game, thinkingTime);

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
        Quadrant quadrants = make_Quadrant();
        game->buildQuadrant(quadrants);
        print(cout, board, quadrants, false);
        cout << "Winner:  " << game->getWinner() << endl << endl;
    } catch (string s) {
        cerr << s << endl;
    } catch (const char* s) {
        cerr << s << endl;
    }
    delete node;
}

int main(int argc, char** argv) {
    try {
        srand(time(NULL));

        bool analysis = false;
        bool selfplay = false;
        string logPath;
        string recordPath;
        for (int i = 0; i < argc; ++i) {
            string arg{argv[i]};
            if (arg == "-a") {
                analysis = true;
                break;
            } else if (arg == "-s") {
                selfplay = true;
                if (i+2 >= argc){
                    cerr << "No paths supplied" << endl;
                    return 1;
                }
                logPath = string{argv[i+1]};
                recordPath = string{argv[i+2]};

                break;
            }
        }
        if (analysis) {
            analyze();
        } else if (selfplay) {
            iterateSelfPlay(logPath, recordPath);
            // std::thread t1(iterateSelfPlay, "Thread1_log.txt");
            // std::thread t2(iterateSelfPlay, "Thread2_log.txt");
            
            // t1.join();
            // t2.join();
        } else {
            // Board2D board = make_Board2D();
            // Quadrant quadrants = make_Quadrant();

            // For(0, 9) {
            //     Forj(0, 9) { board[i][j] = rand() > 0.5 ? P1 : P2; }
            // }
            // print(cout, board, quadrants, false);

            play();

            // cout << sizeof(Node) << endl;
        }
    } catch (...) {
    }
    return 0;
}
