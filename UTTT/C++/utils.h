#pragma once

/* UTTT related utility functions */

#include "UTTT.h"


/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 90 degrees clockwise */
void rotate_90_cw(UTTT& uttt, UTTT& rotated);
void rotate_90_cw(UTTT& uttt);

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 180 degrees clockwise */
void rotate_180_cw(UTTT& uttt, UTTT& rotated);
void rotate_180_cw(UTTT& uttt);

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 180 degrees clockwise */
void rotate_270_cw(UTTT& uttt, UTTT& rotated);
void rotate_270_cw(UTTT& uttt);

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 90 degrees counter clockwise */
void rotate_90_ccw(UTTT& uttt, UTTT& rotated);
void rotate_90_ccw(UTTT& uttt);

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 180 degrees counter clockwise */
void rotate_180_ccw(UTTT& uttt, UTTT& rotated);
void rotate_180_ccw(UTTT& uttt);

/* Fills the rotated UTTT board with a copy of the provided UTTT rotated 180 degrees counter clockwise */
void rotate_270_ccw(UTTT& uttt, UTTT& rotated);
void rotate_270_ccw(UTTT& uttt);
