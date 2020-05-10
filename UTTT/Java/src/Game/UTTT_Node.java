package UI.Game;

import java.lang.reflect.Array;

import static UI.Game.UTTT_Logic.*;

/**
 * Created by Antonio on 2018-04-01.
 */
public abstract class UTTT_Node<T extends UTTT_Node> {

    protected int winner = N, player = N, nextQuadrant = -1;
    protected int capturedQuadrant = N;
    protected int length;

    protected int[] move = null;
    protected T parent = null;
    protected T[] children = null;
    protected boolean initialized = false, moveSet = false;

    public UTTT_Node(){}
    public UTTT_Node(int[] move, T parent, boolean initialize){
        this.move = move;
        if (parent == null){
            this.player = P1;
            this.length = 1;
            initialized = true;
        }
        else{
            this.parent = parent;
            this.winner = parent.winner;
            this.player = parent.player == P1 ? P2 : P1;
            this.length = parent.length+1;
            if (move != null && !capturedQuadrantEquals(move[1], true)){
                nextQuadrant = move[1];
            }
            if (initialize){
                if (this.winner == N){
                    init();
                }
                else{
                    initialized = true;
                }
            }
        }
    }

    public void init(){
        if (!initialized){
            if (move != null) {
                setMove();
            }
            initialized = true;
        }
    }

    public void setMove(int[] move){
        if (this.move == null){
            this.move = move;
            setMove();
        }
    }
    protected void setMove(){
        if (move != null && !moveSet){
            int[] currentQuadrant = new int[9];
            buildQuadrant(currentQuadrant, move[0]);
            capturedQuadrant = check3InRow(currentQuadrant);
            if (capturedQuadrant != N){
                int[] allQuadrants = new int[9];
                buildQuadrant(allQuadrants);
                winner = check3InRow(allQuadrants);
            }
            moveSet = true;
        }
    }

    public boolean isLegal(int... move){
        return (nextQuadrant == -1 || move[0] == nextQuadrant) && !moveOrCapturedQuadrantEquals(move, move[0]);
    }

    public boolean moveEquals(int[] move) {
        return (this.move != null && this.move[0] == move[0] && this.move[1] == move[1]);
    }
    public boolean capturedQuadrantEquals(int quadrant, boolean backpropogate) {
        return (capturedQuadrant != N && move != null && move[0] == quadrant) ||
                (backpropogate && parent != null && parent.capturedQuadrantEquals(quadrant, backpropogate));
    }
    public boolean moveOrCapturedQuadrantEquals(int[] move, int quadrant) {
        return moveEquals(move) || capturedQuadrantEquals(quadrant, false) ||
                (parent != null && parent.moveOrCapturedQuadrantEquals(move, quadrant));
    }

    public boolean hasMove(){
        return move != null;
    }
    public int[] getMove(){
        return move == null ? null : new int[]{move[0], move[1]};
    }
    public int getGlobal(){
        return move[0];
    }
    public int getLocal(){
        return move[1];
    }
    public int getWinner(){
        return winner;
    }
    public int getNextQuadrant(){
        return nextQuadrant;
    }

    public int length(){
        return length;
    }

    public int getPlayer(){
        return player;
    }
    public T getParent(){
        return parent;
    }
    public void initChildren(int num){
        children = getChildArray(num);
    }
    public T[] getChildren(){
        return children;
    }
    public T getChild(int index){
        return children[index];
    }
    public void setChild(int... move){
        if (children != null){
            for (T child : children){
                if (child.move[0] == move[0] && child.move[1] == move[1]){
                    children = getChildArray(child);
                    return;
                }
            }
        }
        if (isLegal(move)){
            children = getChildArray(move, true);
        }
        else{
            System.err.println("Could not find child with move:  "+move[0]+"  "+move[1]);
            System.exit(1);
        }
    }
    protected abstract T[] getChildArray(int num);
    protected abstract T[] getChildArray(T child);
    protected abstract T[] getChildArray(int[] move, boolean initialize);


    public void buildQuadrant(int[] array) {
        if (capturedQuadrant != N) {
            array[move[0]] = capturedQuadrant;
        }
        if (parent != null) {
            parent.buildQuadrant(array);
        }
    }
    public void buildQuadrant(int[] array, int quadrant) {
        UTTT_Node current = this;
        do {
            if (current.move != null && current.move[0] == quadrant) {
                array[current.move[1]] = current.player;
            }
            current = current.parent;
        } while (current != null);
    }
    public void buildBoard2D(int[][] array) {
        UTTT_Node current = this;
        do {
            if (current.move != null) {
                array[current.move[0]][current.move[1]] = current.player;
            }
            current = current.parent;
        } while (current != null);
    }

    public double getConfidence(){
        return 0.5;
    }
    public double getNumSearchInterations(){
        return 0;
    }

    public void printType(){
        System.out.println("UTTT_Node");
    }

//    public void inOrderTraversal(){
//        inOrderTraversal("", 2);
//    }
//    public void inOrderTraversal(String tab, int depth){
//        if (depth <= 0) return;
//        if (move != null && numVisits > 0){
//            System.out.print(move[0]+""+move[1]+""+numWins+"+"+numVisits+(children == null || depth == 1 ? "+0\n" : "+"));
//        }
//        if (children != null){
//            if (depth > 1){
//                int numChildren = 0;
//                for (int i = 0; i<children.length; ++i){
//                    if (children[i].numVisits > 0){
//                        ++numChildren;
//                    }
//                }
//                System.out.println((move != null && numVisits > 0 ? "" : "~")+numChildren);
//            }
//            for (int i = 0; i<children.length; ++i){
//                children[i].inOrderTraversal(tab+"    ", depth-1);
//            }
//        }
//    }
}
