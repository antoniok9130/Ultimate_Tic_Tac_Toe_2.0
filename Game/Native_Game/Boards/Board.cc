//
// Created by Antonio on 2018-04-18.
//

#include "Board.h"
#include <algorithm>
#include <utility>
using namespace std;

const int P1 = 1;
const int P2 = 2;
const int N = 0;
const int T = -1;

Move::Move(int first, int second) : first{first}, second{second} {}
Move::Move(const Move& other) : first{other.first}, second{other.second} {}
Move::Move(Move&& other) : first{std::move(other.first)}, second{std::move(other.second)} {}

string getBoardSymbol(const int& value) { return value == P1 ? "X" : (value == P2 ? "O" : "_"); }

int triple0[2][2] = {{1, 2}, {3, 6}};
int triple4[4][2] = {{3, 5}, {1, 7}, {0, 8}, {2, 6}};
int triple8[2][2] = {{6, 7}, {2, 5}};

int check3InRow(const Quadrant& quadrant) {
    if (quadrant[0] != N) {
        for (const auto& t : triple0) {
            if (quadrant[0] == quadrant[t[0]] && quadrant[t[0]] == quadrant[t[1]]) {
                return quadrant[0];
            }
        }
    }
    if (quadrant[4] != N) {
        for (const auto& t : triple4) {
            if (quadrant[4] == quadrant[t[0]] && quadrant[t[0]] == quadrant[t[1]]) {
                return quadrant[4];
            }
        }
    }
    if (quadrant[8] != N) {
        for (const auto& t : triple8) {
            if (quadrant[8] == quadrant[t[0]] && quadrant[t[0]] == quadrant[t[1]]) {
                return quadrant[8];
            }
        }
    }
    for (auto& e : quadrant) {
        if (e == 0) return N;
    }
    return T;
}

void getRemaining(Quadrant& quadrant, vector<int>& remaining) {
    remaining.reserve(9);
    for (int i = 0; i < 9; ++i) {
        if (quadrant[i] == 0) remaining.emplace_back(i);
    }
}
int& getRandomRemaining(vector<int>& remaining) {
    if (remaining.empty()) {
        throw "Remaining is empty";
    }
    return remaining[rand() % remaining.size()];
}
bool remainingContains(vector<int>& remaining, const int& q) {
    return find(remaining.begin(), remaining.end(), q) != remaining.end();
}
void removeFromRemaining(vector<int>& remaining, const int& n) {
    remaining.erase(remove(remaining.begin(), remaining.end(), n), remaining.end());
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

std::ostream& operator<<(std::ostream& out, std::vector<size_t>& v) {
    out << "[";
    for (auto& e : v) {
        out << e << ", ";
    }
    out << "]";
    return out;
}
template <typename T>
std::ostream& operator<<(std::ostream& out, std::list<T>& l) {
    out << "[";
    for (auto& e : l) {
        out << e << ", ";
    }
    out << "]";
    return out;
}

// Board::Board(int length) : length{length} {}
