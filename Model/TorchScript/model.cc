#include <utility>
#include <vector>

#include "model.h"
#include "torchx.h"

namespace uttt {

    typedef std::shared_ptr<torch::nn::Module> Module;

    struct Model::impl {
        Model* model;
        torch::nn::Sequential blocks;
        torch::nn::Sequential FC;

        impl(Model* model, size_t depth) : model{model} {
            for (size_t d = 1; d <= depth; ++d) {
                std::ostringstream oss;
                oss << "block_" << d;
                const std::string& name = oss.str();
                torchx::nn::Sequential m;
                if (d == 1) {
                    m->push_back(torchx::nn::Conv2dBatch(9, 64, 1, 1));
                    m->push_back(torchx::nn::Conv2dBatch(64, 256, 1, 1));
                } else {
                    m->push_back(torchx::nn::Conv2dBatch(256, 256, 3, 1, 1));
                    m->push_back(torchx::nn::Conv2dBatch(256, 256, 1, 1));
                }
                m = model->register_module(name, m);
                blocks->push_back(m);
            }
            FC = model->register_module(
                "FC",
                torch::nn::Sequential(
                    torchx::nn::Linear(256 * 9, 256),
                    torchx::nn::Dropout(0.5),
                    torchx::nn::ReLU(),
                    torchx::nn::Linear(256, 64),
                    torchx::nn::Dropout(0.5),
                    torchx::nn::ReLU(),
                    torchx::nn::Linear(64, 3)));
        }

        torch::Tensor forward(torch::Tensor x) {
            x = blocks->forward(x);
            x = x.view({-1, 256 * 9});
            x = FC->forward(x);
            return x;
        }
    };

    Model::Model(size_t depth) : self{std::make_unique<Model::impl>(this, depth)} {}
    Model::~Model() = default;

    torch::Tensor Model::forward(torch::Tensor x) { return self->forward(x); }
    torch::Tensor Model::operator()(torch::Tensor x) { return self->forward(x); }

}  // namespace uttt
