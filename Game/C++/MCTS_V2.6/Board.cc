//
// Created by Antonio on 2018-04-18.
//

#include "Board.h"
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <utility>
using namespace std;

Move::Move(int first, int second) : first{first}, second{second} {}
Move::Move(const Move& other) : first{other.first}, second{other.second} {}
Move::Move(const Move* other) : first{other->first}, second{other->second} {}
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

string getBoardSymbol(const int& value, const bool& simple) {
    return value == P1 ? "X" : (value == P2 ? "O" : (simple ? "_" : " "));
}

const int triple0[2][2] = {{1, 2}, {3, 6}};
const int triple4[4][2] = {{3, 5}, {1, 7}, {0, 8}, {2, 6}};
const int triple8[2][2] = {{6, 7}, {2, 5}};

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

int b_seed = time(NULL);
inline int fastrand() {
    b_seed = (214013 * b_seed + 2531011);
    return (b_seed >> 16) & 0x7FFF;
}
int getRandomRemaining(Quadrant& quadrant) {
    int r = 0;
    do {
        r = fastrand() % 9;
    } while (quadrant[r] != N);
    return r;
}


const int pairIndex[10] = {
    0, 3, 5, 8, 10, 14, 16, 19, 21, 24
    // {0, 3}, {3, 2}, {5, 3}, {8, 2}, {10, 4}, {14, 2}, {16, 3}, {19, 2}, {21, 3}
};
const int pairs[24][2] = {
    {1, 2}, {3, 6}, {4, 8},
    {0, 2}, {4, 7}, 
    {0, 1}, {5, 8}, {4, 6}, 
    {0, 6}, {4, 5},
    {0, 8}, {1, 7}, {2, 6}, {3, 5},
    {2, 8}, {3, 4}, 
    {0, 3}, {2, 4}, {7, 8}, 
    {1, 4}, {6, 8},
    {0, 4}, {2, 5}, {6, 7}
};

bool check3InRow(const Quadrant& array, const int& position) {
    const int& start = pairIndex[position];
    const int& end = pairIndex[position+1];
    for (int i = start; i<end; ++i){
        const int& pair0 = pairs[i][0];
        const int& pair1 = pairs[i][1];

        if (array[position] == array[pair0] && array[pair0] == array[pair1]) {
            return true;
        }
    }
    return false;
}

int potential3inRow(const Quadrant& array, const int& position) {
    int potential = N;
    const int& start = pairIndex[position];
    const int& end = pairIndex[position+1];
    for (int i = start; i<end; ++i){
        const int& pair0 = pairs[i][0];
        const int& pair1 = pairs[i][1];

        if (array[pair0] != N && array[pair0] == array[pair1]) {
            if (potential != N && potential != array[pair0]) {
                return B;
            }
            potential = array[pair0];
        }
    }
    return potential;
}
bool potential3inRow(const Quadrant& array, const int& position, const int& player) {
    const int& start = pairIndex[position];
    const int& end = pairIndex[position+1];
    for (int i = start; i<end; ++i){
        const int& pair0 = pairs[i][0];
        const int& pair1 = pairs[i][1];

        if (array[pair0] == player && array[pair0] == array[pair1]) {
            return true;
        }
    }
    return false;
}

void updatePotential3inRow(Quadrant& potential, const Quadrant& array, const int& position) {
    int player = array[position];
    if (player != N) {
        const int& start = pairIndex[position];
        const int& end = pairIndex[position+1];
        for (int i = start; i<end; ++i){
            const int& pair0 = pairs[i][0];
            const int& pair1 = pairs[i][1];

            if (player == array[pair0]) {
                potential[pair1] |= player;
            } else if (player == array[pair1]) {
                potential[pair0] |= player;
            }
        }
    }
}

// void getRemaining(Quadrant& quadrant, vector<int>& remaining) {
//     remaining.reserve(9);
//     for (int i = 0; i < 9; ++i) {
//         if (quadrant[i] == 0) remaining.emplace_back(i);
//     }
// }
// int& getRandomRemaining(vector<int>& remaining) {
//     if (remaining.empty()) {
//         throw "Remaining is empty";
//     }
//     return remaining[rand() % remaining.size()];
// }
// bool remainingContains(vector<int>& remaining, const int& q) {
//     return find(remaining.begin(), remaining.end(), q) != remaining.end();
// }
// void removeFromRemaining(vector<int>& remaining, const int& n) {
//     remaining.erase(remove(remaining.begin(), remaining.end(), n), remaining.end());
// }

Quadrant make_Quadrant() {
    auto quadrant = std::array<int, 9>();
    return quadrant;
}
Board2D make_Board2D() {
    auto board = std::array<Quadrant, 9>();
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
ostream& print(ostream& out, Board2D& board, Quadrant& quadrant, const bool& simple) {
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