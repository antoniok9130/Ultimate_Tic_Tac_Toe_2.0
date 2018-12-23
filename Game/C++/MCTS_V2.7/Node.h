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
#include <list>
#include "Board.h"
// #include "../Boards/Board2D.h"
// #include "../Boards/Quadrants.h"

class Node;

class NodePool {

    size_t max_size;
    Node** pool = nullptr;
    std::list<Node*> stack;
    
    NodePool(const size_t& max_size);
    ~NodePool();
    NodePool(NodePool const&) = delete;
    void operator=(NodePool const&) = delete;

    public:
        static NodePool& getInstance(const size_t& max_size){
            static NodePool instance {max_size};
            return instance;
        }
        static Node* getNode();
        static void returnNode(Node*);
        static size_t maxSize();
        static size_t size();
        static bool empty();
};

class Node {
    int winner = N, player = N, nextQuadrant = -1;
    int numVisits = 0, numWins = 0;
    int length = 0;
    double UCT = 100;
    bool oldUCT = false;

    int local = -1;
    int global = -1;
    bool moveSet = false;
    
    int capturedQuadrant = N;
    Node* parent = nullptr;
    // std::unique_ptr<Quadrants> quadrants;
    // std::unique_ptr<Board2D> board;
    int numChildren = 0;
    std::vector<Node*> children;
    bool initialized = false;


   public:
    Node();

    void reset();
    void init(const int& moveGlobal, const int& moveLocal, Node* parent, const bool& initialize);
    void init();

    // Node(Node* parent = nullptr, bool initialize = true);
    // Node(const int& moveGlobal, const int& moveLocal, Node* parent, const bool& initialize = true);
    // Node(const Move& move, Node* parent = nullptr, const bool& initialize = true);

    bool isLegal(const std::unique_ptr<Move>& move);
    bool isLegal(const int& global, const int& local);

    bool hasMove();
    std::unique_ptr<Move> getMove();
    void setMove(const std::unique_ptr<Move>& move);
    void setMove(const int& global, const int& local);

    int getGlobal();
    int getLocal();
    int getWinner();
    int getNextQuadrant();
    int getCapturedQuadrant();

    bool moveEquals(const int& global, const int& local);
    bool capturedQuadrantEquals(const int& quadrant, const bool& backpropogate = false);
    bool moveOrCapturedQuadrantEquals(const int& global, const int& local, const int& quadrant);

    double getUCT();
    int getNumWins();
    int getNumVisits();
    void incrementWins(const int& i = 1);
    void incrementVisits(const int& i = 1);

    int getLength();

    // void merge(const Node& node);

    int getPlayer();
    Node* getParent();
    void setNumChildren(unsigned int num);
    bool hasNoChildren();
    std::vector<Node*>& getChildren();
    Node* getChild(const int& i);
    void addChild(Node* move);
    void setChild(const std::unique_ptr<Move>& move);
    void setChild(const int& global, const int& local);

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