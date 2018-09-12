package MCTS;


import UI.Game.UTTT_Node;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import static MCTS.MCTS_Logic.*;
import static UI.Game.UTTT_Logic.*;

public class MCTS_Game {

    public static String player1 = "Player 1";
    public static String player2 = "Player 2";

//    private static final int[] double0 = {1, 2, 3, 6, 8};
//    private static final int[] double2 = {0, 1, 5, 8, 6};
//    private static final int[] double4 = {0, 1, 2, 3, 5, 6, 7, 8};
//    private static final int[] double6 = {0, 3, 7, 8, 2};
//    private static final int[] double8 = {0, 2, 5, 7, 8};
//
//    public static boolean has2InRow(final int[] array){
////        boolean a0 = array[0] != N,
////                a2 = array[2] != N,
////                a6 = array[6] != N,
////                a8 = array[8] != N;
////        if ((a0 && a2) || (a2 && a8) || (a8 && a6) || (a6 && a0) || (a6 && a0)){
////            return true;
////        }
////        else if (){
////
////        }
//        if (array[0] != N){
//            for (int row2 : double0){
//                if (array[0] == array[row2]){
//                    return true;
//                }
//            }
//        }
//        if (array[2] != N){
//            for (int row2 : double2){
//                if (array[2] == array[row2]){
//                    return true;
//                }
//            }
//        }
//        if (array[4] != N){
//            for (int row2 : double4){
//                if (array[4] == array[row2]){
//                    return true;
//                }
//            }
//        }
//        if (array[6] != N){
//            for (int row2 : double6){
//                if (array[6] == array[row2]){
//                    return true;
//                }
//            }
//        }
//        if (array[8] != N){
//            for (int row2 : double8){
//                if (array[8] == array[row2]){
//                    return true;
//                }
//            }
//        }
//        return false;
//    }

//    private static class MCTS_Task implements Callable<MCTS_Node> {
//
//        MCTS_Node root;
//        long time;
//
//        public MCTS_Task(MCTS_Node root, long time){
//            this.root = root;
//            this.time = time;
//        }
//
//        @Override
//        public MCTS_Node call() throws Exception {
//            this.root = new MCTS_Node(this.root);
//            long start = System.currentTimeMillis();
//            while (System.currentTimeMillis()-start < time){
//                select(root); select(root); select(root);
//                select(root); select(root); select(root);
//                select(root); select(root); select(root);
//                select(root); select(root); select(root);
//                select(root); select(root); select(root);
//            }
//            return root;
//        }
//    }
//
//    private static int numTasks = 0;

    public static int[] getMove(final MCTS_Node node){
        return getMove(node, 5000); // 3 seconds
    }
    public static int[] getMove(final MCTS_Node node, long thinkingTime) {
        int AIPlayer = node.getPlayer() == P1 ? P2 : P1;
        int[] quadrants = new int[9];
        node.buildQuadrant(quadrants);
        if (node.getNextQuadrant() != -1){
            if (MCTS_Logic.potential3inRow(quadrants, node.getNextQuadrant(), AIPlayer)){
                int[] quadrant = new int[9];
                node.buildQuadrant(quadrant, node.getNextQuadrant());
                for (int i = 0; i<9; ++i){
                    if (quadrant[i] == N && MCTS_Logic.potential3inRow(quadrant, i, AIPlayer)){
                        try {
                            Thread.sleep(750);
                            System.out.println("Instant Win!");
                            return new int[]{node.getNextQuadrant(), i};
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                            System.exit(1);
                        }
                    }
                }
            }
        }
        else{
            for (int i = 0; i<9; ++i){
                if (quadrants[i] == N && MCTS_Logic.potential3inRow(quadrants, i, AIPlayer)){
                    int[] quadrant = new int[9];
                    node.buildQuadrant(quadrant, i);
                    for (int j = 0; j<9; ++j){
                        if (quadrant[j] == N && MCTS_Logic.potential3inRow(quadrant, j, AIPlayer)){
                            try {
                                Thread.sleep(500);
                                System.out.println("Instant Win!");
                                return new int[]{i, j};
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                                System.exit(1);
                            }
                        }
                    }
                }
            }
        }

        long end = System.currentTimeMillis()+thinkingTime;
        while (System.currentTimeMillis() < end){
            select(node); select(node); select(node);
            select(node); select(node); select(node);
            select(node); select(node); select(node);
            select(node); select(node); select(node);
            select(node); select(node); select(node);
        }
        if (node.numVisits() == 0){
            throw new NullPointerException("No Move found...");
        }
        System.out.println("Search Space Size:  "+node.numVisits());
        return getChildVisitedMost(node).getMove();
    }

    public static MCTS_Node getChildVisitedMost(MCTS_Node node){
        int mostVisits = 0;
        int childIndex = -1;
        int i = 0;
        for (MCTS_Node child : node.getChildren()){
            if ((child.numVisits() > mostVisits) ||
                    (child.numVisits() == mostVisits && getRandomBoolean())){
                mostVisits = child.numVisits();
                childIndex = i;
            }
            ++i;
        }
        return node.getChild(childIndex);
    }
    public static MCTS_Node getChildHighestUCT(MCTS_Node node){
        double highestUCT = 0;
        int childIndex = -1;
        int i = 0;
        for (MCTS_Node child : node.getChildren()){
            if ((child.getUCT() > highestUCT) ||
                    (child.getUCT() == highestUCT && getRandomBoolean())){
                highestUCT = child.getUCT();
                childIndex = i;
            }
            ++i;
        }
        return node.getChild(childIndex);
    }

    public static void select(final MCTS_Node node){
//        System.out.println("Selecting...");
        if (node.getChildren() == null){
            node.init();
            if (node.getWinner() != N){
                backpropogate(node, node.getWinner());
            }
            else if (node.hasMove() && node.numVisits() == 0){
                int winner = runSimulation(node);
                backpropogate(node, winner);
            }
            else{
//                System.out.println("Expanding...");
                expand(node);
//                System.out.println("Expanded.");
            }
        }
        else{
            select(getChildHighestUCT(node));
        }
    }

    public static void expand(final MCTS_Node node){
        if (node.getChildren() == null){
            int numChildren = 0;
            List<int[]> legalMoves = new LinkedList<>();
            int[] allQuadrants = new int[9];
            node.buildQuadrant(allQuadrants);
            if (node.hasMove() && allQuadrants[node.getLocal()] == N){
                int[] nextQuadrant = new int[9];
                node.buildQuadrant(nextQuadrant, node.getLocal());
                for (int i = 0; i < 9; ++i) {
                    if (nextQuadrant[i] == N) {
                        legalMoves.add(new int[]{node.getLocal(), i});
                    }
                }
            }
            else{
                int[][] board = new int[9][9];
                node.buildBoard2D(board);
                for (int i = 0; i < 9; ++i) {
                    if (allQuadrants[i] == N) {
                        for (int j = 0; j < 9; ++j) {
                            if (board[i][j] == 0) {
                                legalMoves.add(new int[]{i, j});
                            }
                        }
                    }
                }
            }

            if (!legalMoves.isEmpty()){
                node.initChildren(legalMoves.size());

                int i = -1;
                for (int[] legalMove : legalMoves) {
                    node.getChildren()[++i] = new MCTS_Node(legalMove, node, false);
                }

                MCTS_Node random = (MCTS_Node) Tools.random(node.getChildren());
                int winner = runSimulation(random);
                backpropogate(random, winner);
            }
        }
    }

    public static int runSimulation(final MCTS_Node node){
        node.init();
        int[][] board = new int[9][9];
        node.buildBoard2D(board);
        int[] quadrants = new int[9];
        node.buildQuadrant(quadrants);

        int numRemainingQuadrants = 0;
        int[] numRemainingBoard = new int[9];
        int[] potentialQuadrants = new int[9];
        for (int i = 0; i<9; ++i){
            if (quadrants[i] == N){
                ++numRemainingQuadrants;
                potentialQuadrants[i] = MCTS_Logic.potential3inRow(quadrants, i);
                for (int j = 0; j<9; ++j){
                    if (board[i][j] == N){
                        ++numRemainingBoard[i];
                    }
                }
            }
        }

        int[] move = node.getMove();
        if (move == null){
            move = new int[]{-1, -1};
        }
        int player = node.getPlayer();
        int winner = node.getWinner();
        while (winner == N){
            if (move[1] != -1 && quadrants[move[1]] == N){
                move[0] = move[1];
            }
            else{
                move[0] = getRandomRemaining(quadrants);
            }

            if (potentialQuadrants[move[0]] == player || potentialQuadrants[move[0]] == B){
                for (int i = 0; i<9; ++i){
                    if(board[move[0]][i] == N && MCTS_Logic.potential3inRow(board[move[0]], i, player)){
                        return player;
                    }
                }
            }

            move[1] = getRandomRemaining(board[move[0]]);
            player = player == P2 ? P1 : P2;
            board[move[0]][move[1]] = player;
            --numRemainingBoard[move[0]];

            if (check3InRow(board[move[0]], move[1])) {
                quadrants[move[0]] = player;
                --numRemainingQuadrants;

                updatePotential3inRow(potentialQuadrants, quadrants, move[0]);

                if (check3InRow(quadrants, move[0])){
                    winner = player;
                    return player;
                }
                else if (numRemainingQuadrants <= 0){
                    winner = T;
                    return T;
                }
            }
            else if (numRemainingBoard[move[0]] <= 0){
                quadrants[move[0]] = T;
                --numRemainingQuadrants;
                if (numRemainingQuadrants <= 0){
                    winner = T;
                    return T;
                }
            }
        }
        return winner;
    }

    public static void backpropogate(final MCTS_Node node, int winner){
        if (node.getPlayer() == winner){
            node.incrementWins();
        }
        node.incrementVisits();

        if (node.getParent() != null){
            backpropogate((MCTS_Node) node.getParent(), winner);
        }

        node.updateUCT();
    }

}
