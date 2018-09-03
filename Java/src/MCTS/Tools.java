package MCTS;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.List;

/**
 * Created by Antonio on 2018-04-01.
 */
public class Tools {

    public static int randomint(int low, int high){
        return (int)((high-low+1)*Math.random()+low);
    }
    public static<E> E random(List<E> list){
        return list.get(randomint(0, list.size()-1));
    }
    public static<E> E random(E[] array){
        return array[randomint(0, array.length-1)];
    }
    public static int random(int[] array){
        return array[randomint(0, array.length-1)];
    }

    public static<E> void print(List<E> list){
        System.out.print("[");
        for (int i = 0; i<list.size(); ++i){
            if (i > 0){
                System.out.print(", ");
            }
            System.out.print(list.get(i));
        }
        System.out.println("]");
    }

    public static int readInt(BufferedReader br){
        try {
            return Integer.parseInt(br.readLine().trim());
        } catch (IOException | NumberFormatException e) {
            e.printStackTrace();
            System.exit(1);
        }
        return -1;
    }
    public static double readDouble(BufferedReader br){
        try {
            return Double.parseDouble(br.readLine().trim());
        } catch (IOException | NumberFormatException e) {
            e.printStackTrace();
            System.exit(1);
        }
        return -1;
    }

}
