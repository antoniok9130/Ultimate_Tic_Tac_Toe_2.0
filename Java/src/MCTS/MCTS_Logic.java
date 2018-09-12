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
	

}
