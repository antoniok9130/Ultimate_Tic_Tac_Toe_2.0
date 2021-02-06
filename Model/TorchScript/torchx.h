#pragma once

#include <memory>

#include <torch/torch.h>

namespace torchx {

    namespace nn {

        struct SequentialImpl: public torch::nn::SequentialImpl {
            using torch::nn::SequentialImpl::SequentialImpl;

            torch::Tensor forward(torch::Tensor x) {
                return torch::nn::SequentialImpl::forward(x);
            }
        };

        TORCH_MODULE(Sequential);

        inline torch::nn::Linear Linear(
            size_t in_channels, size_t out_channels, bool bias = true) {
            return torch::nn::Linear(
                torch::nn::LinearOptions(in_channels, out_channels).bias(bias));
        }
        inline torch::nn::Dropout Dropout(double p) {
            return torch::nn::Dropout(torch::nn::DropoutOptions().p(p));
        }
        inline torch::nn::ReLU ReLU(bool inplace = true) {
            return torch::nn::ReLU(torch::nn::ReLUOptions().inplace(inplace));
        }

        torchx::nn::Sequential Conv2dBatch(
            size_t in_channels,
            size_t out_channels,
            size_t kernel_size = 3,
            size_t stride = 1,
            size_t padding = 0,
            bool bias = true,
            double leaky = 0) {
            using namespace torch::nn;
            torchx::nn::Sequential m(
                Conv2d(Conv2dOptions(in_channels, out_channels, kernel_size)
                           .stride(stride)
                           .padding(padding)
                           .bias(bias)),
                BatchNorm2d(out_channels));
            if (leaky == 0) {
                m->push_back(torchx::nn::ReLU());
            } else {
                m->push_back(
                    LeakyReLU(LeakyReLUOptions().negative_slope(leaky).inplace(true)));
            }
            return m;
        }

    }  // namespace nn

}  // namespace torchx
