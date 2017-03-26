#!/usr/bin/env python

from math import sin, cos, pi

SAMPLING_RATE = 2 * (10 ** 6) # 2 Msps
ACCUMULATOR_BITS = 32
LOOKUP_TABLE_INDEX_BITS = 18 # keep smaller than ACCUMULATOR_BITS

class NCO(object):
    def __init__(self,
                 sampling_rate=SAMPLING_RATE,
                 accumulator_bits=ACCUMULATOR_BITS,
                 lookup_table_index_bits=LOOKUP_TABLE_INDEX_BITS):
        self.sampling_rate = sampling_rate
        self.accumulator_bits = accumulator_bits
        self.lookup_table_index_bits = lookup_table_index_bits

        self.lookup_table = []
        self.lookup_table_size = 2 ** self.lookup_table_index_bits
        for i in range(self.lookup_table_size):
            self.lookup_table.append(sin((2 * pi * i) / self.lookup_table_size))

        self.sample_time = 1.0 / self.sampling_rate
        
        self.accumulator_size = 2 ** self.accumulator_bits
        self.accumulator_shift = self.accumulator_bits - self.lookup_table_index_bits

        self.accumulator = 0
        
    def run(self, frequency, seconds):
        phase_per_sample = int(self.accumulator_size * frequency * self.sample_time)
        while seconds >= 0:
            seconds -= self.sample_time

            self.accumulator += phase_per_sample
            self.accumulator %= self.accumulator_size # overflow

            yield self.lookup_table[self.accumulator >> self.accumulator_shift]

class QuadratureNCO(NCO):
    def __init__(self,
                 sampling_rate=SAMPLING_RATE,
                 accumulator_bits=ACCUMULATOR_BITS,
                 lookup_table_index_bits=LOOKUP_TABLE_INDEX_BITS):
        super(QuadratureNCO, self).__init__(sampling_rate,
                                            accumulator_bits,
                                            lookup_table_index_bits)

        self.iaccumulator = 0
        self.qaccumulator = 0

    def run(self, frequency, seconds):
        self.qaccumulator = self.iaccumulator + (3 * (self.accumulator_size >> 2)) 
        self.qaccumulator %= self.accumulator_size # overflow

        phase_per_sample = int(self.accumulator_size * frequency * self.sample_time)
        while seconds >= 0:
            seconds -= self.sample_time

            self.iaccumulator += phase_per_sample
            self.iaccumulator %= self.accumulator_size # overflow

            self.qaccumulator += phase_per_sample
            self.qaccumulator %= self.accumulator_size # overflow

            yield self.lookup_table[self.iaccumulator >> self.accumulator_shift], \
                  self.lookup_table[self.qaccumulator >> self.accumulator_shift]

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Numerically Controlled Oscillator (accumulator bits: %d, lookup table index bits: %d)' % (ACCUMULATOR_BITS, LOOKUP_TABLE_INDEX_BITS))
    parser.add_argument('frequency', type=int, nargs='?', default=1000)
    parser.add_argument('seconds', type=float, nargs='?', default=0.01)
    args = parser.parse_args()

    frequency = args.frequency
    seconds = args.seconds

    nco = NCO()
    for s in nco.run(frequency, seconds):
        print s

    nco = QuadratureNCO()
    for i, q in nco.run(frequency, seconds):
        print i, q
