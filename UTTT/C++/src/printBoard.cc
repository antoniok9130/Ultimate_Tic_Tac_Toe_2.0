
#include <sstream>
#include <string>

#include "../UTTT.h"

using namespace std;

static char getBoardSymbol(const int& player){
    switch(player){
        case P1:
            return 'X';
        case P2:
            return 'O';
        case N:
            return ' ';
        case T:
            return 'T';
        default:
            throw "Invalid player given to getBoardSymbol";
    }
}

const char* verticalSpace = "     │   │    ║    │   │    ║    │   │    ";
const char* verticalDivide = "  ───┼───┼─── ║ ───┼───┼─── ║ ───┼───┼─── ";
const char* bigVerticalDivide = " ═════════════╬═════════════╬═════════════";

const char* verticalSpace2 = "    ║   ║   ";
const char* bigVerticalDivide2 = " ═══╬═══╬═══ ";
const char* minDivide = "  ";

std::ostream& operator<<(std::ostream& out, UTTT& u){

    string endls[23];
    unsigned int i = 6;
    endls[i++] = verticalSpace2;
    ostringstream r1;
    r1 << "  ";
    for (int j = 0; j<3; ++j){
        r1 << getBoardSymbol(u.getPlayerAt(j));
        if (j != 2){
            r1 << " ║ ";
        }
    }
    r1 << " ";
    endls[i++] = r1.str();
    endls[i++] = bigVerticalDivide2;
    ostringstream r2;
    r2 << "  ";
    for (int j = 3; j<6; ++j){
        r2 << getBoardSymbol(u.getPlayerAt(j));
        if (j != 5){
            r2 << " ║ ";
        }
    }
    r2 << " ";
    endls[i++] = r2.str();
    endls[i++] = bigVerticalDivide2;
    ostringstream r3;
    r3 << "  ";
    for (int j = 6; j<9; ++j){
        r3 << getBoardSymbol(u.getPlayerAt(j));
        if (j != 8){
            r3 << " ║ ";
        }
    }
    r3 << " ";
    endls[i++] = r3.str();
    endls[i++] = verticalSpace2;
    i = 0;


    out << endl;
    for (int a = 0; a < 3; ++a) {
        if (a != 0) {
            out << bigVerticalDivide << minDivide << " " << endls[i++] << endl;
        }
        out << verticalSpace << minDivide << " " << endls[i++] << endl;
        for (int b = 0; b < 3; ++b) {
            if (b != 0) {
                out << verticalDivide << minDivide << " " << endls[i++] << endl;
            }
            out << "  ";
            for (int c = 0; c < 3; ++c) {
                if (c != 0) {
                    out << " ║ ";
                }
                for (int d = 0; d < 3; ++d) {
                    if (d != 0) {
                        out << "│";
                    }
                    out << " " << getBoardSymbol(u.getPlayerAt(3 * a + c, 3 * b + d)) << " ";
                }
            }
            out << minDivide << "  " << endls[i++] << endl;
        }
        out << verticalSpace << minDivide << " " << endls[i++] << endl;
    }
    out << endl;

    return out;
}
