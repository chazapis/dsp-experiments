#!/usr/bin/env python

class QuadratureMixer(object):
    def run(self, quadrature_generator_1, quadrature_generator_2):
        try:
            while True:
                i1, q1 = quadrature_generator_1.next()
                i2, q2 = quadrature_generator_2.next()

                yield i1 * i2, q1 * q2
        except StopIteration:
            return

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='SSB generator')
    parser.add_argument('base_frequency', type=int, nargs='?', default=1000)
    parser.add_argument('mix_frequency', type=int, nargs='?', default=8000)
    parser.add_argument('seconds', type=float, nargs='?', default=0.01)
    args = parser.parse_args()

    base_frequency = args.base_frequency
    mix_frequency = args.mix_frequency
    seconds = args.seconds

    from nco import NCO, QuadratureNCO
    from hilbert import Hilbert

    nco = NCO()
    base_signal_generator = nco.run(base_frequency, seconds)
    hilbert = Hilbert()
    quadrature_generator_1 = hilbert.run(base_signal_generator)

    quadrature_nco = QuadratureNCO()
    quadrature_generator_2 = quadrature_nco.run(mix_frequency, seconds)

    quadrature_mixer = QuadratureMixer()
    for i, q in quadrature_mixer.run(quadrature_generator_1, quadrature_generator_2):
        # print i, q
        print i + q
