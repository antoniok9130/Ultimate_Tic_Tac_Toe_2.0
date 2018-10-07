package MCTS_Variant;

import MCTS_Variant.MCTS_Game;
import MCTS.MCTS_Node;
import UI.UTTT_App;
import javafx.application.Application;
import javafx.stage.Stage;

/**
 * Created by Antonio on 2018-04-01.
 */
public class UTTT_MCTS_Variant extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception {
        UTTT_App<MCTS_Node> uttt_app = new UTTT_App<MCTS_Node>(primaryStage){
            @Override
            public void resetGame() {
                this.game = new MCTS_Node();
            }

            @Override
            public void setMove(int... move) {
                System.out.println("Setting Move:  "+move[0]+", "+move[1]);
                game.setChild(move);
                game = game.getChild(0);
                setGameStarted(true);
            }

            @Override
            protected int[] get_AI_move() {
                return MCTS_Game.getMove(game, 3200);
            }
        };
        uttt_app.start();
    }

    public static void main(String[] args){
        Application.launch(args);
    }

}
