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
    exit(1);
}
void incrementNumPlayer2Wins(){
    ++numPlayer2Wins;
}
void incrementNumTies(){
    ++numTies;
}

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

void travel();

void subtravel(int* board, int* quadrants, int* numFilledBoard, int numFilledQuadrants, int global, int length){
    int player = (length%2)+1;
    int* quadrant = board + 9*global;
    int* numFilledQuadrant = numFilledBoard + global;
    for (int i = 0; i<9; ++i){
        if (quadrant[i] == 0){
            incrementNumStates();

            quadrant[i] = player;
            ++(*numFilledQuadrant);
            int filled = check3InRow(quadrant, i);
            int winner = 0;
            if (filled){
                quadrants[global] = player;
                winner = check3InRow(quadrants, global);
                if (winner != 0){
                    if (player == 1){
                        incrementNumPlayer1Wins();
                    }
                    else {
                        incrementNumPlayer2Wins();
                    }
                }
                else if (numFilledQuadrants >= 8){
                    winner = -1;
                    incrementNumTies();
                }
            }

            if (winner == 0){
                travel(board, quadrants, numFilledBoard, numFilledQuadrants+filled, i, length+1);
            }

            quadrant[i] = 0;
            --(*numFilledQuadrant);
            if (filled){
                quadrants[global] = 0;
            }
        }
    }
}

void travel(int* board, int* quadrants, int* numFilledBoard, int numFilledQuadrants, int previousLocal, int length){
    if (previousLocal != -1 && quadrants[previousLocal] == 0){
        subtravel(board, quadrants, numFilledBoard, numFilledQuadrants, previousLocal, length);
    }
    else{
        for (int i = 0; i<9; ++i){
            if (quadrants[i] == 0){
                subtravel(board, quadrants, numFilledBoard, numFilledQuadrants, i, length);
            }
        }
    }
}



int main(){
    int* board = (int*) calloc(81, sizeof(int));
    int* quadrants = (int*) calloc(9, sizeof(int));
    int* numFilledBoard = (int*) calloc(9, sizeof(int));

    travel(board, quadrants, numFilledBoard, 0, -1, 0);

    printf("\n\nNum States:         %llu\n", numStates);
    printf("Num Wrap Arounds:   %llu\n", numWrapArounds);
    printf("Num Extreme Wraps:  %llu\n", numExtremeWraps);
    printf("Num Player 1 Wins:  %llu\n", numPlayer1Wins);
    printf("Num Player 2 Wins:  %llu\n", numPlayer2Wins);
    printf("Num Ties:           %llu\n\n", numTies);

    free(board);
    free(quadrants);
    free(numFilledBoard);
}
