
#include <iostream>
#include <cmath>

using namespace std;

double calculateUCT(int numWins, int numVisits, int numParentVisits){
	return numWins/numVisits+sqrt(2*log(numParentVisits)/numVisits);
}

double numVisitsDerivative(int numWins, int numVisits, int numParentVisits){
	return (sqrt(numVisits*log(1000*sqrt(2)))+numWins)/(numVisits*numVisits);
}


int main(){
	int numParentVisits = 2000000;
	double origUCT = calculateUCT(1, 1, numParentVisits);
	double update_1 = calculateUCT(1, 2, numParentVisits);
	double update_2 = calculateUCT(2, 2, numParentVisits);
	cout << origUCT << endl;
	cout << "  + " << update_1-origUCT << " = " << update_1 << endl;
	cout << "  + " << update_2-origUCT << " = " << update_2 << endl << endl;

	double orig_deriv = numVisitsDerivative(1, 1, numParentVisits);
	cout << orig_deriv << endl;
	double update_1_deriv = numVisitsDerivative(1, 2, numParentVisits);
	cout << update_1_deriv << endl;
	double update_2_deriv = numVisitsDerivative(2, 2, numParentVisits);
	cout << update_2_deriv << endl;
}
