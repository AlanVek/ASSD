#pragma once
#include <vector>
#include <complex>

using vcomplex = std::vector<std::complex<double>>;

void fft(const vcomplex& in, vcomplex& out);
void ifft(const vcomplex& in, vcomplex& out);