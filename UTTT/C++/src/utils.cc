
#include "../utils.h"

const int rot_90_cw_new_quadrant[9] = {2, 5, 8, 1, 4, 7, 0, 3, 6};

int rotate_90_cw_quadrant(int quadrant){
    return ((quadrant & 0b001000000) >> 6) |
           ((quadrant & 0b100001000) >> 2) |
           ((quadrant & 0b000100001) << 2) |
           ((quadrant & 0b010000000) >> 4) |
           ((quadrant & 0b000010000))      |
           ((quadrant & 0b000000010) << 4) |
           ((quadrant & 0b000000100) << 6);
}

void rotate_90_cw(UTTT& uttt, UTTT& rotated){
    for (int player = 0; player < 2; ++player){
        for (int q = 0; q < 9; ++q){
            rotated.setQuadrant(
                rot_90_cw_new_quadrant[q],
                player,
                rotate_90_cw_quadrant(
                    uttt.getQuadrant(q, player)
                )
            );
        }
        rotated.setBoard(
            player,
            rotate_90_cw_quadrant(
                uttt.getBoard(player)
            )
        );
    }
}

void rotate_90_cw(UTTT& uttt){
    UTTT rotated = uttt;
    rotate_90_cw(uttt, rotated);
    uttt = rotated;
}

int rotate_180_cw_quadrant(int quadrant){
    return ((quadrant & 0b100000000) >> 8) |
           ((quadrant & 0b010000000) >> 6) |
           ((quadrant & 0b001000000) >> 4) |
           ((quadrant & 0b000100000) >> 2) |
           ((quadrant & 0b000010000))      |
           ((quadrant & 0b000001000) << 2) |
           ((quadrant & 0b000000100) << 4) |
           ((quadrant & 0b000000010) << 6) |
           ((quadrant & 0b000000001) << 8) ;
}

/* Returns a copy of the provided UTTT board rotated 180 degrees clockwise */
void rotate_180_cw(UTTT& uttt, UTTT& rotated){
    for (int player = 0; player < 2; ++player){
        for (int q = 0; q < 9; ++q){
            rotated.setQuadrant(
                8 - q,
                player,
                rotate_180_cw_quadrant(
                    uttt.getQuadrant(q, player)
                )
            );
        }
        rotated.setBoard(
            player,
            rotate_180_cw_quadrant(
                uttt.getBoard(player)
            )
        );
    }
}

void rotate_180_cw(UTTT& uttt){
    UTTT rotated = uttt;
    rotate_180_cw(uttt, rotated);
    uttt = rotated;
}

int rotate_270_cw_quadrant(int quadrant){
    return ((quadrant & 0b010000100) >> 2) |
           ((quadrant & 0b000100000) >> 4) |
           ((quadrant & 0b100000000) >> 6) |
           ((quadrant & 0b000000010) << 2) |
           ((quadrant & 0b000010000)) |
           ((quadrant & 0b000000001) << 6) |
           ((quadrant & 0b000001000) << 4);
}

const int rot_270_cw_new_quadrant[9] = {6, 3, 0, 7, 4, 1, 8, 5, 2};

/* Returns a copy of the provided UTTT board rotated 180 degrees clockwise */
void rotate_270_cw(UTTT& uttt, UTTT& rotated){
    for (int player = 0; player < 2; ++player){
        for (int q = 0; q < 9; ++q){
            rotated.setQuadrant(
                rot_270_cw_new_quadrant[q],
                player,
                rotate_270_cw_quadrant(
                    uttt.getQuadrant(q, player)
                )
            );
        }
        rotated.setBoard(
            player,
            rotate_270_cw_quadrant(
                uttt.getBoard(player)
            )
        );
    }
}

void rotate_270_cw(UTTT& uttt){
    UTTT rotated = uttt;
    rotate_270_cw(uttt, rotated);
    uttt = rotated;
}


/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 90 degrees counter clockwise */
void rotate_90_ccw(UTTT& uttt, UTTT& rotated){ rotate_270_cw(uttt, rotated); }
void rotate_90_ccw(UTTT& uttt){
    UTTT rotated = uttt;
    rotate_270_cw(uttt, rotated);
    uttt = rotated;
}

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 180 degrees counter clockwise */
void rotate_180_ccw(UTTT& uttt, UTTT& rotated){ rotate_180_cw(uttt, rotated); }
void rotate_180_ccw(UTTT& uttt){
    UTTT rotated = uttt;
    rotate_180_cw(uttt, rotated);
    uttt = rotated;
}

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 180 degrees counter clockwise */
void rotate_270_ccw(UTTT& uttt, UTTT& rotated){ rotate_90_cw(uttt, rotated); }
void rotate_270_ccw(UTTT& uttt){
    UTTT rotated = uttt;
    rotate_90_cw(uttt, rotated);
    uttt = rotated;
}
