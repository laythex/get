import time
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt


dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

########################################
#   Open, use and close SPI ADC
########################################


def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    _value = [0, 0, 0, 0, 0, 0, 0, 0]
    _dec_value = 0
    for i in range(8):
        _value[i] = 1
        GPIO.output(dac, _value)
        time.sleep(0.0007)
        _comp_value = GPIO.input(comp)
        if _comp_value == 0:
            _value[i] = 0
        _dec_value += _value[i] * 2 ** (7 - i)
    return _dec_value


########################################
#   Setup, use and cleanup GPIO
########################################

def waitForOpen():
    GPIO.setup(22, GPIO.IN)

    print('GPIO initialized. Wait for door opening...')
    print(GPIO.input(22))
    while GPIO.input(22) == 1:
        print(GPIO.input(22))

    print('The door is open. GPIO has been cleaned up. Start sampling...')


########################################
#   Save and read data
########################################

def save(samples, start, finish):
    filename = 'wave-data {}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))

    with open(filename, "w") as outfile:
        outfile.write('- Wave Lab\n')
        outfile.write('- Date: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Duration: {:.2f} s\n\n'.format(finish - start))
        
        np.savetxt(outfile, np.array(samples).T, fmt='%d')

def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    duration = float(lines[2].split()[2])
    samples = np.asarray(lines[4:], dtype=int)
    
    return samples, duration, len(samples)



length = 144.5
t = 15
dt = 0.0007
data = []
waitForOpen()
t0 = time.time()
while ((time.time() - t0) < t):
    data.append(adc())
    time.sleep(dt)
save(data, 0, t)

