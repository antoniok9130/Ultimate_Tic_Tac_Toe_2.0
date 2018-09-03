package MCTS;

import UI.Menus.Menus;
import UI.UTTT_App;
import javafx.application.Application;
import javafx.stage.Stage;

import java.awt.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import static UI.Custom.centerStage;

/**
 * Created by Antonio on 2018-04-01.
 */
public class UTTT_MCTS extends Application {

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
                return MCTS_Game.getMove(game, (long)(difficulty*1000));
            }
        };
        uttt_app.start();
    }

    public static void main(String[] args){
        Application.launch(args);
    }

}
