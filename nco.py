#!/usr/bin/env python

import sys

from math import sin, cos, pi

SAMPLING_RATE = 2 * (10 ** 6) # 2 Msps

ACCUMULATOR_BITS = 32
LOOKUP_TABLE_INDEX_BITS = 18 # keep smaller than ACCUMULATOR_BITS

accumulator = 0

lookup_table = []
lookup_table_size = 2 ** LOOKUP_TABLE_INDEX_BITS
for i in range(lookup_table_size):
    lookup_table.append(sin((2 * pi * i) / lookup_table_size))

frequency = 20 * (10 ** 6) # 20 MHz 
frequency = 5000

if __name__ == '__main__':
    seconds = 0.02

    sample_time = 1.0 / SAMPLING_RATE
    accumulator_size = 2 ** ACCUMULATOR_BITS
    accumulator_shift = ACCUMULATOR_BITS - LOOKUP_TABLE_INDEX_BITS
    phase_per_sample = int(accumulator_size * frequency * sample_time)
    while seconds >= 0:
        seconds -= sample_time

        accumulator += phase_per_sample
        accumulator %= accumulator_size # overflow
        
        print lookup_table[accumulator >> accumulator_shift]

    # for i in range(lookup_table_size):
    #     print lookup_table[i]
    # sys.exit(0)

    # print 'Numerically Controlled Oscillator'
    # print '(accumulator bits: %d, lookup table index bits: %d)' % (ACCUMULATOR_BITS, LOOKUP_TABLE_INDEX_BITS)
    # print

    # while True:
    #     try:
    #         frequency = raw_input('Enter frequency: ')
    #         if not frequency.isdigit():
    #             raise ValueError
    #         frequency = int(frequency)

    #         seconds = raw_input('Enter time in seconds: ')
    #         if not seconds.isdigit():
    #             raise ValueError
    #         seconds = int(seconds)

    #         print 'Running for frequency: %d, seconds: %d' % (frequency, seconds)

    #     except ValueError:
    #         print 'Wrong input'
    #     except (KeyboardInterrupt, EOFError):
    #         break

