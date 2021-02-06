#pragma once

#include <iostream>
#include <memory>

#include <torch/torch.h>

namespace uttt {

    class Model: public torch::nn::Module {
      public:
        Model(size_t depth = 3);
        ~Model();

        torch::Tensor forward(torch::Tensor);
        torch::Tensor operator()(torch::Tensor);

      private:
        struct impl;
        std::unique_ptr<impl> self;  // in keeping with python semantics
    };

}  // namespace uttt
