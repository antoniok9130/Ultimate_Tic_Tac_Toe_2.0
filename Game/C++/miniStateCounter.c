#include <stdio.h>
#include <stdlib.h>

unsigned long long numStates = 0;
unsigned long long numWrapArounds = 0;
int numExtremeWraps = 0;

void incrementNumStates(){
    ++numStates;
    if (numStates == 0){
        ++numWrapArounds;
        if (numWrapArounds == 0){
            ++numExtremeWraps;
        }
    }
}

unsigned long long numPlayer1Wins = 0;
unsigned long long numPlayer2Wins = 0;
unsigned long long numTies = 0;

void incrementNumPlayer1Wins(){
    ++numPlayer1Wins;
}
void incrementNumPlayer2Wins(){
    ++numPlayer2Wins;
}
void incrementNumTies(){
    ++numTies;
}

int* player1WinsFirstGrid;
int* player2WinsFirstGrid;

const int pairIndex[9][2] = {
    {0, 3}, {3, 2}, {5, 3}, {8, 2}, {10, 4}, {14, 2}, {16, 3}, {19, 2}, {21, 3}
};
const int pairs[24][2] = {
    {1, 2}, {3, 6}, {4, 8},
    {0, 2}, {4, 7}, 
    {0, 1}, {5, 8}, {4, 6}, 
    {0, 6}, {4, 5},
    {0, 8}, {1, 7}, {2, 6}, {3, 5},
    {2, 8}, {3, 4}, 
    {0, 3}, {2, 4}, {7, 8}, 
    {1, 4}, {6, 8},
    {0, 4}, {2, 5}, {6, 7}
};

int check3InRow(const int* quadrant, const int position) {
    int start = pairIndex[position][0];
    int end = start+pairIndex[position][1];
    for (int i = start; i<end; ++i){
        int pair0 = pairs[i][0];
        int pair1 = pairs[i][1];

        if (quadrant[position] == quadrant[pair0] && quadrant[pair0] == quadrant[pair1]) {
            return 1;
        }
    }
    return 0;
}

void travel(int* board, int numFilledBoard, int first){
    int player = (numFilledBoard%2)+1;
    for (int i = 0; i<9; ++i){
        if (board[i] == 0){
            incrementNumStates();

            board[i] = player;
            int winner = check3InRow(board, i);
            if (winner != 0){
                if (player == 1){
                    incrementNumPlayer1Wins();
                    ++player1WinsFirstGrid[first];
                }
                else {
                    incrementNumPlayer2Wins();
                    ++player2WinsFirstGrid[first];
                }
                // for (int j = 0; j<9; ++j){
                //     if (board[i] == 1){
                //         ++player1WinsGrid[j];
                //     }
                //     else if (board[i] == 2){
                //         ++player2WinsGrid[j];
                //     }
                // }
            }
            else if (numFilledBoard >= 8){
                winner = -1;
                incrementNumTies();
            }

            if (winner == 0){
                travel(board, numFilledBoard+1, first == -1 ? i : first);
            }

            board[i] = 0;
        }
    }
}



int main(){
    int* board = (int*) calloc(9, sizeof(int));
    player1WinsFirstGrid = (int*) calloc(9, sizeof(int));
    player2WinsFirstGrid = (int*) calloc(9, sizeof(int));

    travel(board, 0, -1);

    printf("\n\nNum States:         %llu\n", numStates);
    printf("Num Player 1 Wins:  %llu\n", numPlayer1Wins);
    printf("Num Player 2 Wins:  %llu\n", numPlayer2Wins);
    printf("Num Ties:           %llu\n\n", numTies);

    printf("Player 1 Wins First Grid:\n");
    for (int i = 0; i<9; ++i){
        printf("    %i\n", player1WinsFirstGrid[i]);
    }
    printf("Player 2 Wins First Grid:\n");
    for (int i = 0; i<9; ++i){
        printf("    %i\n", player2WinsFirstGrid[i]);
    }



    fflush(stdout);
    free(board);
    free(player1WinsFirstGrid);
    free(player2WinsFirstGrid);
}

/*
Num States:         549945
Num Player 1 Wins:  131184
Num Player 2 Wins:  77904
Num Ties:           46080

    14652
    14232
    14652
    14232
    15648
    14232
    14652
    14232
    14652

    7896
    10176
    7896
    10176
    5616
    10176
    7896
    10176
    7896

Rewards:
    If win:  reward = 1000
    If captured quadrant:  
        if captured == 4:
            reward = 150*0.3513877661 = 52.708164915117             // 15648/(14652+14232+15648) = 0.3513877661
        else if captured is corner:
            reward = 150*0.329021827 = 49.3532740501215          // 14652/(14652+14232+15648) = 0.329021827
        else:
            reward = 150*0.3195904 = 47.9385610347615            // 14232/(14652+14232+15648) = 0.3195904
    
        If first captured quadrant:
            reward *= 1.6839        // 131184/77904 =   1.6839
*/
