#pragma once

#include "eigen-3.4-rc1/Eigen/Dense"

void fft(const Eigen::VectorXcd& in, Eigen::VectorXcd& out);

void ifft(const Eigen::VectorXcd& in, Eigen::VectorXcd& out);