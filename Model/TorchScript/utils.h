#pragma once

#include <torch/torch.h>

static int numTrainableParameters(const torch::nn::Module& module) {
    int num;
    for (auto& param : module.parameters()) {
        if (param.requires_grad()) {
            long size = 1;
            for (size_t dim = 0; dim < param.dim(); ++dim) { size *= param.size(dim); }
            num += size;
        }
    }
    return num;
}
