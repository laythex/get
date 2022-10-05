import RPi.GPIO as GPIO
from time import sleep

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for _value in range(256):
        GPIO.output(dac, dec2bin(_value))
        sleep(0.0007)
        _comp_value = GPIO.input(comp)
        if _comp_value == 0:
            return _value

try:
    while True:
        value = adc()
        voltage = 3.3 / 256 * value
        print(value, '{:.2f}'.format(voltage), 'V')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()