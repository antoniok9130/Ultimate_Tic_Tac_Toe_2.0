package MCTS;

import java.util.SplittableRandom;

import static UI.Game.UTTT_Logic.*;


public class MCTS_Logic {

    public static int potential3inRow(int[] array, int position){
        int potential = N;
        for (int[] pair : pairs[position]){
            if (array[pair[0]] != N && array[pair[0]] == array[pair[1]]){
                if (potential != N && potential != array[pair[0]]){
                    return B;
                }
                potential = array[pair[0]];
            }
        }
        return potential;
    }
    public static boolean potential3inRow(int[] array, int position, int player){
        for (int[] pair : pairs[position]){
            if (array[pair[0]] == player && array[pair[0]] == array[pair[1]]){
                return true;
            }
        }
        return false;
    }

    public static void updatePotential3inRow(int[] potential, int[] array, int position){
        int player = array[position];
        if (player != N){
            for (int[] pair : pairs[position]){
                if (player == array[pair[0]]){
                    potential[pair[1]] |= player;
                }
                else if (player == array[pair[1]]){
                    potential[pair[0]] |= player;
                }
            }
        }
	}

    public static int[] isPotentialWin(MCTS_Node node, int AIPlayer){
        int[] quadrants = new int[9];
        node.buildQuadrant(quadrants);
        if (node.getNextQuadrant() != -1){
            if (potential3inRow(quadrants, node.getNextQuadrant(), AIPlayer)){
                int[] quadrant = new int[9];
                node.buildQuadrant(quadrant, node.getNextQuadrant());
                for (int i = 0; i<9; ++i){
                    if (quadrant[i] == N && MCTS_Logic.potential3inRow(quadrant, i, AIPlayer)){
//                            System.out.println("Instant Win!");
                        return new int[]{node.getNextQuadrant(), i};
                    }
                }
            }
        }
        else{
            for (int i = 0; i<9; ++i){
                if (quadrants[i] == N && potential3inRow(quadrants, i, AIPlayer)){
                    int[] quadrant = new int[9];
                    node.buildQuadrant(quadrant, i);
                    for (int j = 0; j<9; ++j){
                        if (quadrant[j] == N && potential3inRow(quadrant, j, AIPlayer)){
//                                System.out.println("Instant Win!");
                            return new int[]{i, j};
                        }
                    }
                }
            }
        }
        return null;
    }

    static int[][][][] preAnalyzed = {
        {{{0, 5, 1}, {0, 6, 2}, {0, 2, 5}, {0, 7, 1}, {0, 8, 1}}, {{1, 5, 8}, {1, 3, 1}, {1, 7, 1}}, {{2, 2, 4}, {2, 6, 4}, {2, 8, 2}}, {{3, 7, 10}}, {{4, 4, 10}}, {{5, 1, 1}, {5, 7, 9}}, {{6, 6, 7}, {6, 2, 2}, {6, 8, 1}}, {{7, 5, 9}, {7, 7, 1}}, {{8, 8, 10}}},
        {{{0, 8, 10}}, {{1, 5, 3}, {1, 3, 7}}, {{2, 6, 10}}, {{3, 5, 5}, {3, 3, 3}, {3, 7, 2}}, {{4, 4, 10}}, {{5, 7, 5}, {5, 3, 5}}, {{6, 6, 10}}, {{7, 5, 3}, {7, 3, 7}}, {{8, 8, 10}}},
        {{{0, 0, 4}, {0, 8, 4}, {0, 6, 2}}, {{1, 5, 1}, {1, 3, 9}}, {{2, 0, 3}, {2, 3, 2}, {2, 6, 2}, {2, 7, 1}, {2, 8, 2}}, {{3, 7, 7}, {3, 3, 1}, {3, 1, 2}}, {{4, 4, 10}}, {{5, 7, 9}, {5, 1, 1}}, {{6, 6, 10}}, {{7, 3, 9}, {7, 5, 1}}, {{8, 8, 9}, {8, 0, 1}}},
        {{{0, 8, 10}}, {{1, 1, 5}, {1, 7, 4}, {1, 5, 1}}, {{2, 2, 10}}, {{3, 1, 8}, {3, 7, 2}}, {{4, 4, 9}}, {{5, 1, 5}, {5, 7, 4}}, {{6, 2, 9}}, {{7, 7, 4}, {7, 1, 3}, {7, 5, 2}}, {{8, 8, 8}, {8, 0, 1}}},
        {{{0, 0, 8}, {0, 8, 1}}, {{1, 5, 4}, {1, 3, 5}}, {{2, 2, 9}}, {{3, 1, 5}, {3, 7, 4}}, {{4, 8, 8}, {4, 6, 5}, {4, 0, 6}, {4, 2, 10}}, {{5, 1, 7}, {5, 7, 2}}, {{6, 6, 9}}, {{7, 5, 7}, {7, 3, 2}}, {{8, 8, 8}, {8, 0, 1}}},
        {{{0, 0, 9}}, {{1, 1, 3}, {1, 7, 4}, {1, 3, 2}}, {{2, 2, 1}, {2, 6, 7}, {2, 0, 1}}, {{3, 7, 6}, {3, 1, 3}}, {{4, 4, 9}}, {{5, 7, 5}, {5, 1, 4}}, {{6, 6, 8}, {6, 2, 1}}, {{7, 1, 4}, {7, 7, 3}, {7, 3, 2}}, {{8, 0, 9}}},
        {{{0, 0, 6}, {0, 8, 2}, {0, 2, 1}}, {{1, 5, 7}, {1, 3, 2}}, {{2, 2, 9}}, {{3, 1, 9}}, {{4, 4, 9}}, {{5, 1, 9}}, {{6, 5, 2}, {6, 2, 2}, {6, 0, 1}, {6, 8, 2}, {6, 1, 2}}, {{7, 5, 9}}, {{8, 8, 7}, {8, 2, 2}}},
        {{{0, 0, 9}}, {{1, 3, 4}, {1, 5, 5}}, {{2, 2, 9}}, {{3, 5, 3}, {3, 1, 1}, {3, 3, 5}}, {{4, 4, 9}}, {{5, 3, 3}, {5, 5, 3}, {5, 1, 3}}, {{6, 2, 9}}, {{7, 3, 3}, {7, 5, 5}, {7, 1, 1}}, {{8, 0, 9}}},
        {{{0, 0, 9}}, {{1, 3, 6}, {1, 1, 1}, {1, 5, 2}}, {{2, 4, 1}, {2, 2, 6}, {2, 0, 2}}, {{3, 1, 8}, {3, 3, 1}}, {{4, 4, 9}}, {{5, 1, 9}}, {{6, 2, 5}, {6, 0, 1}, {6, 6, 3}}, {{7, 3, 9}}, {{8, 3, 1}, {8, 0, 4}, {8, 1, 1}, {8, 2, 2}, {8, 6, 1}}}
    };

    public static int[] getPreAnalyzedMove(int[] move){
        int[][] precomputed = preAnalyzed[move[0]][move[1]];
        int sum = 0;
        for (int i = 0; i<precomputed.length; ++i){
            sum += precomputed[i][2];
        }
        int r = getRandomInt(sum);
        sum = 0;
        for (int i = 0; i<precomputed.length; ++i){
            sum += precomputed[i][2];
            if (r < sum){
                return new int[]{precomputed[i][0], precomputed[i][1]};
            }
        }
        return null;
    }


}
