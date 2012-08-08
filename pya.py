import pyaudio
import wave
import sys
import dsp

chunk = 1024

d = dsp.tone(dsp.stf(10), dsp.randint(100, 800))

p = pyaudio.PyAudio()

# open stream
stream = p.open(format = p.get_format_from_width(2),
                channels = 2,
                rate = 44100,
                output = True)

# read data
data = dsp.cut(d, dsp.randint(0, 100) * chunk, chunk) 

#play stream
for i in range(1100):
    stream.write(data)
    data = dsp.cut(d, i * chunk, chunk) 

stream.close()
p.terminate()
