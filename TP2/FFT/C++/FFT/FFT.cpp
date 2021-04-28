#include "FFT.h"
#define _USE_MATH_DEFINES
#include <algorithm>
#include <math.h>

void bitreverse_indices(int n, std::vector<int>& out) {
	out[0] = 0;
	out[1] = n / 2;

	auto gamma = std::log2(n);
	auto t = out.begin();

	for (int i = 1; i < gamma; ++i) {
		t = out.begin() + static_cast<int>(std::pow(2, i));
		std::transform(out.begin(), t, t, [&i, &gamma](auto v) {return v + std::pow(2, gamma - i - 1); });
	}
}

void fft(const vcomplex& in, vcomplex& out) {
	auto n = in.size();

	if (n <= 1) { out = in; return; }
	else if (n & (n - 1)) {
		throw std::exception("Size must have shape 2^k");
	}

	auto gamma = std::log2(n);
	std::vector<int>bitrev_idx(n);
	bitreverse_indices(n, bitrev_idx);

	vcomplex W(n), temp(n);

	temp[0] = in[0];
	temp[n / 2] = in[1];
	W[0] = 1;

	std::transform(bitrev_idx.begin(), bitrev_idx.end(), W.begin(), [&n](auto v) {return std::exp(std::complex<double>(0, -2 * M_PI / n * v)); });
	std::transform(bitrev_idx.begin(), bitrev_idx.end(), temp.begin(), [&in](auto& v) {return in[v]; });
	out = temp;

	auto t = bitrev_idx.begin();
	int n_groups = 0, dist_buts = 0;
	for (int stage = 0; stage < gamma; ++stage) {
		n_groups = static_cast<int>(std::pow(2, stage));
		dist_buts = n / n_groups;

		//#pragma loop(hint_parallel(8))
		for (int group = 0; group < n_groups; ++group) {
			t = bitrev_idx.begin() + group * dist_buts;

			std::for_each(t, t + dist_buts / 2, [&out, &dist_buts, &group, &W](int& v) {
				out[*(&v + dist_buts / 2)] *= W[2 * group];

				out[v] += out[*(&v + dist_buts / 2)];

				out[*(&v + dist_buts / 2)] *= -2;
				out[*(&v + dist_buts / 2)] += out[v];
				});
		}
	}
}

void conj(const vcomplex& in, vcomplex& out, double k = 1) {
	std::transform(in.begin(), in.end(), out.begin(), [&k](auto v) {return std::complex<double>(v.real() / k, -v.imag() / k); });
}

void ifft(const vcomplex& in, vcomplex& out) {
	auto n = in.size();

	conj(in, out);
	fft(out, out);
	conj(out, out, n);
}