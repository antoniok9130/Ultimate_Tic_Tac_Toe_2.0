#ifndef UTTT_MCTS_H
#define UTTT_MCTS_H

#include <array>
#include <iostream>
#include <list>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#define For(a, b) for (int i = a; i < b; ++i)
#define Forj(a, b) for (int j = a; j < b; ++j)

///////////////////////////////////////////////////////////////
////////////////////////// Board.h ////////////////////////////
///////////////////////////////////////////////////////////////

#ifndef P1
#define P1 1
#endif
#ifndef P2
#define P2 2
#endif
#ifndef N
#define N 0
#endif
#ifndef TIE
#define TIE -1
#endif

typedef std::array<int, 9> Quadrant;
typedef std::array<Quadrant, 9> Board2D;
typedef unsigned int uint;

struct Move {
    int first;
    int second;

    Move(int first, int second);
    Move(const Move& other);
    Move(Move&& other);
    Move& operator=(const Move& other);
    Move& operator=(Move&& other);
};

std::string getBoardSymbol(const int& value, bool simple = true);

int check3InRow(const Quadrant& quadrant);

int getRandomRemaining(Quadrant& quadrant);

Quadrant make_Quadrant();
Board2D make_Board2D();

std::ostream& operator<<(std::ostream& out, Quadrant& quadrant);
std::ostream& operator<<(std::ostream& out, Board2D& board);
std::ostream& print(std::ostream& out, Board2D& board, Quadrant& quadrant, bool simple = true);


///////////////////////////////////////////////////////////////
////////////////////////// Node.h /////////////////////////////
///////////////////////////////////////////////////////////////

class Node {
    int winner = N, player = N, nextQuadrant = -1;
    int numVisits = 0, numWins = 0;
    int length = 0;
    double UCT = 100;
    std::unique_ptr<Move> move;
    int capturedQuadrant = N;
    Node* parent = nullptr;
    // std::unique_ptr<Quadrants> quadrants;
    // std::unique_ptr<Board2D> board;
    int numChildren = 0;
    std::vector<std::unique_ptr<Node>> children;
    bool initialized = false, moveSet = false;

   public:
    Node();
    // Node(const Node& other);

    // Node(Node* parent = nullptr, bool initialize = true);
    Node(int moveGlobal, int moveLocal, Node* parent = nullptr, bool initialize = true);
    Node(const Move& move, Node* parent = nullptr, bool initialize = true);

    void init();

    void updateUCT();
    bool isLegal(const Move& move);

    bool hasMove();
    std::unique_ptr<Move>& getMove();
    // void setMove(int moveGlobal, int moveLocal);
    void setMove(std::unique_ptr<Move>& move);
    void setMove();

    int getGlobal();
    int getLocal();
    int getWinner();
    int getNextQuadrant();
    int getCapturedQuadrant();

    bool moveEquals(const Move& move);
    bool capturedQuadrantEquals(const int& quadrant, const bool& backpropogate = false);
    bool moveOrCapturedQuadrantEquals(const Move& move, const int& quadrant);

    double getUCT();
    int getNumWins();
    int getNumVisits();
    void incrementWins(const int& i = 1);
    void incrementVisits(const int& i = 1);

    int getLength();

    void merge(const Node& node);

    int getPlayer();
    Node* getParent();
    void setNumChildren(unsigned int num);
    std::vector<std::unique_ptr<Node>>& getChildren();
    void addChild(std::unique_ptr<Node>& move);
    void setChild(const Move& move);

    void buildQuadrant(Quadrant& array);
    void buildQuadrant(Quadrant& array, const int& quadrant);
    void buildBoard2D(Board2D& array);

    std::ostream& printTrace(std::ostream& out);
};

///////////////////////////////////////////////////////////////
////////////////////////// Game.h /////////////////////////////
///////////////////////////////////////////////////////////////

Move getMove(Node* node, double duration = 3.0);

Move getChildVisitedMost(Node* node);
std::unique_ptr<Node>& getChildHighestUCT(Node* node);

void select(Node* node);
void expand(Node* node);
int runSimulation(Node* node);
void backpropogate(Node* node, int winner);




extern "C" {
Node* Node_new();
void Node_delete(Node* node);
int Node_getWinner(Node* node);
int Node_getNumWins(Node* node);
int Node_getNumVisits(Node* node);
Node* Node_setMove(Node* node, int first, int second);

void MCTS_select(Node* node);
void MCTS_expand(Node* node);
int MCTS_runSimulation(Node* node);
void MCTS_backpropogate(Node* node, int winner);
}

#endif  // UTTT_MCTS_H