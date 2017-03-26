#!/usr/bin/env python

from math import pi

class Hilbert(object):
    def __init__(self, length=101):
        assert(length % 2 == 1)
        self.length = length
        self.half_length = (self.length - 1) / 2

        # Inspired by: https://epxx.co/artigos/ammodulation.html
        self.impulse = [1.0 / (pi * float(t)) for t in range(-self.half_length, 0)] + \
                       [0] + \
                       [1.0 / (pi * float(t)) for t in range(1, self.half_length + 1)]

        self.buffer = []
        
    def run(self, signal_generator):
        for s in signal_generator:
            self.buffer.insert(0, s)
            if len(self.buffer) == self.length - 1:
                break

        for s in signal_generator:
            self.buffer.insert(0, s)
            convolution = sum([self.buffer[i] * self.impulse[i] for i in range(self.length)])

            # yield self.buffer[self.half_length], convolution
            yield convolution, self.buffer[self.half_length]
            self.buffer.pop()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Hilbert transform')
    parser.add_argument('frequency', type=int, nargs='?', default=1000)
    parser.add_argument('seconds', type=float, nargs='?', default=0.01)
    args = parser.parse_args()

    frequency = args.frequency
    seconds = args.seconds

    from nco import NCO

    nco = NCO()
    signal_generator = nco.run(frequency, seconds)

    hilbert = Hilbert(1001)
    for s, t in hilbert.run(signal_generator):
        print s, t
