package MCTS;


import UI.Game.UTTT_Node;
import UI.Game.UTTT_Simple;

/**
 * Created by Antonio on 2018-04-01.
 */
public class MCTS_Node extends UTTT_Node<MCTS_Node> {

    public static final int UCT_MAX = 100;

    private int numVisits = 0, numWins = 0;
    private double UCT = UCT_MAX;

    public MCTS_Node(){
        super();
    }
    public MCTS_Node(int[] move, MCTS_Node parent, boolean initialize){
        super(move, parent, initialize);
    }


    @Override
    protected MCTS_Node[] getChildArray(int num) {
        return new MCTS_Node[num];
    }

    @Override
    protected MCTS_Node[] getChildArray(MCTS_Node child) {
        return new MCTS_Node[]{child};
    }

    @Override
    protected MCTS_Node[] getChildArray(int[] move, boolean initialize) {
        return new MCTS_Node[]{new MCTS_Node(move, this, initialize)};
    }

    public void updateUCT(){
        if (parent != null && numVisits != 0){
            UCT = numWins/(double)numVisits+Math.sqrt(2*Math.log(parent.numVisits)/numVisits);
        }
    }

    public double getUCT(){
        return UCT;
    }
    public int numWins(){
        return numWins;
    }
    public int numVisits(){
        return numVisits;
    }
    public void incrementWins(){
        ++numWins;
    }
    public void incrementWins(int i){
        numWins += i;
    }
    public void incrementVisits(){
        ++numVisits;
    }
    public void incrementVisits(int i){
        numVisits += i;
    }


    @Override
    public double getConfidence(){
        return numWins/(double)numVisits;
    }
    @Override
    public double getNumSearchInterations(){
        return numVisits;
    }

    @Override
    public void printType(){
        System.out.println("MCTS_Node");
    }

}
