package UI.Game;

import java.util.SplittableRandom;

public class UTTT_Logic {

    public static final int P1 = 1;
    public static final int P2 = 2;
    public static final int N = 0;
    public static final int T = -1;
    public static final int B = 3; // Note that (P1 | P2) == B

    public static final int[][] triple0 = {{1, 2}, {3, 6}};
    public static final int[][] triple4 = {{3, 5}, {1, 7}, {0, 8}, {2, 6}};
    public static final int[][] triple8 = {{6, 7}, {2, 5}};

    public static int check3InRow(final int[] array){
        boolean checkTie = true;
        if (array[0] != N){
            for (int[] triple : triple0){
                if (array[0] == array[triple[0]] && array[triple[0]] == array[triple[1]]){
                    return array[0];
                }
            }
        }
        else{
            checkTie = false;
        }
        if (array[4] != N){
            for (int[] triple : triple4){
                if (array[4] == array[triple[0]] && array[triple[0]] == array[triple[1]]){
                    return array[4];
                }
            }
        }
        else{
            checkTie = false;
        }
        if (array[8] != N){
            for (int[] triple : triple8){
                if (array[8] == array[triple[0]] && array[triple[0]] == array[triple[1]]){
                    return array[8];
                }
            }
        }
        else{
            checkTie = false;
        }

        return (checkTie && array[1] != N && array[2] != N && array[3] != N && array[5] != N && array[6] != N && array[7] != N)
                ? T : N;
    }

    public static boolean check3InRow(int[] array, int position){
        for (int[] pair : pairs[position]){
            if (array[position] == array[pair[0]] && array[pair[0]] == array[pair[1]]){
                return true;
            }
        }
        return false;
    }

    public static boolean checkTie(int[] array){
        for (int i : array){
            if (i == N)    return false;
        }
        return true;
    }

    public static final int[][][] pairs = {
            {{1, 2}, {3, 6}, {4, 8}},
            {{0, 2}, {4, 7}},
            {{0, 1}, {5, 8}, {4, 6}},
            {{0, 6}, {4, 5}},
            {{0, 8}, {1, 7}, {2, 6}, {3, 5}},
            {{2, 8}, {3, 4}},
            {{0, 3}, {2, 4}, {7, 8}},
            {{1, 4}, {6, 8}},
            {{6, 7}, {2, 5}, {0, 4}}};


    public static String getBoardSymbol(int value, boolean simple){
        switch(value){
            case P1: return "X";
            case P2: return "O";
            case T:  return "T";
            default: return simple ? "_" : " ";
        }
    }

    private static final SplittableRandom fastrand = new SplittableRandom(System.currentTimeMillis());
    public static int getRandomRemaining(int[] quadrant) {
        int r = 0;
        int i = 0;
        do {
            r = fastrand.nextInt(9);
            ++i;
        } while (quadrant[r] != N && i < 1000);
        if (quadrant[r] != N){
            System.err.println("Could not find Random Remaining:");
            for (int j = 0; j<9; ++j){
                System.err.println("     "+quadrant[j]);
            }
            throw new NullPointerException("Could not find Random Remaining:");
        }
        return r;
    }
    public static boolean getRandomBoolean(){
        return fastrand.nextBoolean();
    }
    public static int getRandomInt(int i){
        return fastrand.nextInt(i);
    }

    private static final String verticalSpace = "     │   │    ║    │   │    ║    │   │    ";
    private static final String verticalDivide = "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ";
    private static final String bigVerticalDivide = " ═════════════╬═════════════╬═════════════";

    public static void print(int[][] board, int[] quadrant, boolean simple){
        if (simple) {
            for (int a = 0; a < 3; ++a) {
                for (int b = 0; b < 3; ++b) {
                    for (int c = 0; c < 3; ++c) {
                        for (int d = 0; d < 3; ++d) {
                            System.out.print(getBoardSymbol(board[3 * a + c][3 * b + d], simple));
                        }
                        System.out.print("  ");
                    }
                    if (a == 0) {
                        System.out.print("   ");
                        for (int d = 0; d < 3; ++d) {
                            System.out.print(getBoardSymbol(quadrant[3 * b + d], simple));
                        }
                    }
                    System.out.println();
                }
                System.out.println();
            }
        } else {
            System.out.println();
            for (int a = 0; a < 3; ++a) {
                if (a != 0) {
                    System.out.println(bigVerticalDivide);
                }
                System.out.println(verticalSpace);
                for (int b = 0; b < 3; ++b) {
                    if (b != 0) {
                        System.out.println(verticalDivide);
                    }
                    System.out.print("  ");
                    for (int c = 0; c < 3; ++c) {
                        if (c != 0) {
                            System.out.print(" ║ ");
                        }
                        for (int d = 0; d < 3; ++d) {
                            if (d != 0) {
                                System.out.print("│");
                            }
                            System.out.print(" "+getBoardSymbol(board[3 * a + c][3 * b + d], simple)+" ");
                        }
                    }
                    System.out.println(" ");
                }
                System.out.println(verticalSpace);
            }
            System.out.println();
        }
    }

}
