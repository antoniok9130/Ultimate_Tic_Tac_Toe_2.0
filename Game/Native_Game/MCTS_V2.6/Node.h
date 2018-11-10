//
// Created by Antonio on 2018-04-18.
//

#ifndef ULTIMATE_TIC_TAC_TOE_ZERO_NODE_H
#define ULTIMATE_TIC_TAC_TOE_ZERO_NODE_H

#include <array>
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>
#include "Board.h"
// #include "../Boards/Board2D.h"
// #include "../Boards/Quadrants.h"

class Node;

typedef std::pair<std::unique_ptr<Move>, std::unique_ptr<Node>> Child;

class Node {
    s_int winner = N, length = 0, nextQuadrant = -1;
    s_int capturedQuadrant = N;
    Move* move = nullptr;
    unsigned int numVisits = 0, numWins = 0;
    double UCT = 100;
    Node* parent = nullptr;
    // std::unique_ptr<Quadrants> quadrants;
    // std::unique_ptr<Board2D> board;
    // s_int numChildren = 0;
    std::vector<Child> children;
    bool initialized = false, moveSet = false, oldUCT = true;


    void addChild(std::unique_ptr<Move>& move, std::unique_ptr<Node>& node);

   public:
    Node();
    // Node(const Node& other);

    // Node(Node* parent = nullptr, bool initialize = true);
    // Node(const s_int& moveGlobal, const s_int& moveLocal, Node* parent, const bool& initialize = true);
    Node(Move* move, Node* parent = nullptr, const bool& initialize = true);

    void init();
    
    bool isLegal(const Move& move);

    bool hasMove();
    Move* getMove();
    // void setMove(int moveGlobal, int moveLocal);
    // void setMove(std::unique_ptr<Move>& move);
    void setMove();

    s_int getGlobal();
    s_int getLocal();
    s_int getWinner();
    s_int getNextQuadrant();
    s_int getCapturedQuadrant();

    bool moveEquals(const Move& move);
    bool capturedQuadrantEquals(const int& quadrant, const bool& backpropogate = false);
    bool moveOrCapturedQuadrantEquals(const Move& move, const int& quadrant);

    double getUCT();
    unsigned int getNumWins();
    unsigned int getNumVisits();
    void incrementWins(const int& i = 1);
    void incrementVisits(const int& i = 1);

    int getLength();

    void merge(const Node& node);

    int getPlayer();
    Node* getParent();
    void setNumChildren(unsigned int num);
    bool hasNoChildren();
    std::vector<Child>& getChildren();
    std::unique_ptr<Node>& getChild(const int& i);
    std::unique_ptr<Node>& back();
    void addChild(std::unique_ptr<Move>& move);
    void setChild(const Move& move);

    void buildQuadrant(Quadrant& array);
    void buildQuadrant(Quadrant& array, const int& quadrant);
    void buildBoard2D(Board2D& array);

    std::ostream& printTrace(std::ostream& out);

    // Quadrants& getQuadrants();

    // Board2D& getBoard();
};

// std::ostream& operatora<<(std::ostream& out, Node& node);

// extern "C" {
// Node* Node_new();
// void Node_delete(Node* node);
// int Node_getWinner(Node* node);
// int Node_getNumWins(Node* node);
// int Node_getNumVisits(Node* node);
// }

#endif  // ULTIMATE_TIC_TAC_TOE_ZERO_NODE_H