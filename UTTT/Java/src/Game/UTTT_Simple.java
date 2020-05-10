package UI.Game;

public class UTTT_Simple extends UTTT_Node<UTTT_Simple> {

    public UTTT_Simple() {
    }

    public UTTT_Simple(int[] move, UTTT_Simple parent, boolean initialize) {
        super(move, parent, initialize);
    }

    @Override
    protected UTTT_Simple[] getChildArray(int num) {
        return new UTTT_Simple[num];
    }

    @Override
    protected UTTT_Simple[] getChildArray(UTTT_Simple child) {
        return new UTTT_Simple[]{child};
    }

    @Override
    protected UTTT_Simple[] getChildArray(int[] move, boolean initialize) {
        return new UTTT_Simple[]{new UTTT_Simple(move, this, initialize)};
    }

}
