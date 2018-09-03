//
// Created by Antonio on 2018-04-18.
//

#ifndef ULTIMATE_TIC_TAC_TOE_ZERO_NODE_H
#define ULTIMATE_TIC_TAC_TOE_ZERO_NODE_H

#include <memory>
#include <array>
#include <string>
#include <utility>
#include <vector>
#include "Board.h"
// #include "../Boards/Board2D.h"
// #include "../Boards/Quadrants.h"

class Node {
    int winner = N, player = N, nextQuadrant = -1;
    int numVisits = 0, numWins = 0;
    int length = 0;
    double UCT = 100;
    std::unique_ptr<Move> move;
    int capturedQuadrant = N;
    Node* parent = nullptr;
    int numChildren = 0;
    std::vector<std::unique_ptr<Node>> children;
    bool initialized = false, moveSet = false;

    std::unique_ptr<Quadrant> quadrants;
    std::unique_ptr<Board2D> board;

	// int numQuadrantBuild1 = 0, numQuadrantBuild2 = 0, numBoard2DBuild2 = 0;

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

    bool moveEquals(const Move& move, bool backpropogate = false);
    bool capturedQuadrantEquals(const int& quadrant, bool backpropogate = false);
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
    void setChild(std::unique_ptr<Node>& move);

	void buildQuadrant();
	// void buildQuadrant(Quadrant& array, const int& quadrant);
	void buildBoard2D();

    Quadrant& getQuadrants();

    Board2D& getBoard();
};

// std::ostream& operatora<<(std::ostream& out, Node& node);

#endif  // ULTIMATE_TIC_TAC_TOE_ZERO_NODE_H
