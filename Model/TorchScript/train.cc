
#include <iostream>

#include <torch/torch.h>

#include "model.h"
#include "utils.h"

using namespace std;

int main() {
    uttt::Model model;
    cout << "Model: " << endl << model << endl;
    cout << "Num Parameters: " << numTrainableParameters(model) << endl;

    torch::Tensor input = torch::rand({1, 9, 3, 3});

    auto output = model.forward(input);

    std::cout << "output: " << endl << output << std::endl;
}
