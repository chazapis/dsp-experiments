#!/usr/bin/env python

import wave
import struct

from nco import QuadratureNCO
from hilbert import Hilbert
from mixer import QuadratureMixer

# Load signal

# Samples from: http://www-mobile.ecs.soton.ac.uk/hth97r/links/demo.html
wav_in = wave.open('man1_wb.wav', 'r')

nchannels = wav_in.getnchannels()
sampwidth = wav_in.getsampwidth()
framerate = wav_in.getframerate()
nframes = wav_in.getnframes()

print 'Nchannels:', nchannels
print 'Sampwidth:', sampwidth
print 'Framerate:', framerate
print 'Nframes:', nframes

assert(nchannels == 1)
assert(sampwidth == 2)

base_signal = [struct.unpack('h', wav_in.readframes(1))[0] / 32768.0 for i in range(nframes)]
base_signal_generator = iter(base_signal)

wav_in.close()

# Upconvert

mix_frequency = 500
seconds = (len(base_signal) / framerate) + 1

print 'Seconds:', seconds

hilbert = Hilbert()
quadrature_generator_1 = hilbert.run(base_signal_generator)
print 'Signal transformed'

quadrature_nco = QuadratureNCO(sampling_rate=framerate)
quadrature_generator_2 = quadrature_nco.run(mix_frequency, seconds)
print 'Mix frequency generated'

quadrature_mixer = QuadratureMixer()
upconverted_signal = [i + q for i, q in quadrature_mixer.run(quadrature_generator_1, quadrature_generator_2)]
print 'Mixed'

# Save output

wav_out = wave.open('upconverted.wav', 'w')

wav_out.setnchannels(1)
wav_out.setsampwidth(2)
wav_out.setframerate(framerate)

for f in upconverted_signal:
    wav_out.writeframes(struct.pack('h', f * 32767.0))

wav_out.close()
