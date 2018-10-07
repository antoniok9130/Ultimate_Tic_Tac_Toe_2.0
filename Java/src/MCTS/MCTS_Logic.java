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

    public static Tools.Pair<Boolean, int[]> isPotentialWin(MCTS_Node node, int AIPlayer){
        int[] quadrants = new int[9];
        node.buildQuadrant(quadrants);
        if (node.getNextQuadrant() != -1){
            if (potential3inRow(quadrants, node.getNextQuadrant(), AIPlayer)){
                int[] quadrant = new int[9];
                node.buildQuadrant(quadrant, node.getNextQuadrant());
                for (int i = 0; i<9; ++i){
                    if (quadrant[i] == N && MCTS_Logic.potential3inRow(quadrant, i, AIPlayer)){
//                            System.out.println("Instant Win!");
                        return new Tools.Pair<>(true, new int[]{node.getNextQuadrant(), i});
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
                            return new Tools.Pair<>(true, new int[]{i, j});
                        }
                    }
                }
            }
        }
        return new Tools.Pair<>(false, null);
    }
	

}
