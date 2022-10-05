import RPi.GPIO as GPIO
from time import sleep
from math import ceil

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    _value = [0, 0, 0, 0, 0, 0, 0, 0]
    _dec_value = 0
    for i in range(8):
        _value[i] = 1
        GPIO.output(dac, _value)
        sleep(0.0007)
        _comp_value = GPIO.input(comp)
        if _comp_value == 0:
            _value[i] = 0
        _dec_value += _value[i] * 2 ** (7 - i)
    return _dec_value

try:
    while True:
        value = adc()
        leds_value = 2 ** ceil(value / 32) - 1
        GPIO.output(leds, dec2bin(leds_value))
        voltage = 3.3 / 256 * value
        print(value, '{:.2f}'.format(voltage), 'V', leds_value)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()