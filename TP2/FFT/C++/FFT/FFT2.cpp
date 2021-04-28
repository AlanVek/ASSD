#include "FFT2.h"
#define _USE_MATH_DEFINES
#include <math.h>

using complex = std::complex<double>;

void bitreverse_indices(int n, Eigen::VectorXi& out) {
	out(0) = 0;
	out(1) = n / 2;

	auto gamma = std::log2(n);
	int t = 0;

	for (int i = 1; i < gamma; ++i) {
		t = static_cast<int>(std::pow(2, i));
		out(Eigen::seqN(t, t)) = out(Eigen::seqN(0, t)).array() + int(std::pow(2, gamma - i - 1));
	}
}
//
void fft(const Eigen::VectorXcd& in, Eigen::VectorXcd& out) {
	auto n = in.size();

	/* Chequeamos que tenga el tamaño correcto */
	if (n <= 1) { out = in; return; }
	else if (n & (n - 1)) {
		throw std::exception("Size must have shape 2^k");
	}

	int gamma = static_cast<int>(std::log2(n));

	/* Definimos un vector con los índices en bit-reverse */
	Eigen::VectorXi bitrev_idx(n);
	bitreverse_indices(n, bitrev_idx);

	/* Creamos el vector de W, cuyos exponentes son los índices en bit-reverse saltando de a dos */
	auto by2 = Eigen::Map<Eigen::VectorXi, 0, Eigen::InnerStride<>>(bitrev_idx.data(), n / 2, Eigen::InnerStride<>(2));
	Eigen::VectorXcd W = Eigen::exp(complex(0, -2 * M_PI / n) * by2.array().cast<complex>());

	/* Copiamos el vector in al vector out */
	Eigen::VectorXcd temp = in;
	out = temp;

	int n_groups = 0, dist_buts = 0;

	/* Vamos por cada una de las etapas... */
	for (int stage = 0; stage < gamma; ++stage) {
		n_groups = static_cast<int>(std::pow(2, stage));
		dist_buts = n / n_groups;

		/* Separamos cada grupo en una columna de la matriz grouped */
		auto grouped = out.reshaped(dist_buts, n_groups);

		/* Nos quedamos con los primeros (mitad superior de la matriz) y los segundos (mitad inferior) de cada mariposa */
		auto firsts = grouped.topRows(dist_buts / 2);
		auto seconds = grouped.bottomRows(dist_buts / 2);

		/* Multiplicamos a cada uno de los segundos por su W correspondiente y reemplazamos por la mariposa */
		seconds *= W.head(n_groups).asDiagonal();
		firsts += seconds;
		seconds = -2 * seconds + firsts;
	}

	/* Devolvemos en out el bit-reverse del resultado obtenido */
	Eigen::VectorXcd temp2 = out(bitrev_idx);
	out = temp2;
}

void ifft(const Eigen::VectorXcd& in, Eigen::VectorXcd& out) {
	fft(in.conjugate(), out);
	out = out.conjugate() / in.size();
}