#include <iostream>
#include "FFT2.h"
#include <complex>

int main()
{
	try {
		srand(time(NULL));

		int N = std::pow(2, 12);
		auto a = Eigen::VectorXcd(Eigen::VectorXi::Random(N).cast<std::complex<double>>());

		fft(a, a);
		ifft(a, a);
	}
	catch (std::exception& e) {
		std::cout << e.what();
	}
}