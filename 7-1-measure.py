import RPi.GPIO as GPIO
import time
from matplotlib import pyplot as plt

# Настройка GPIO на Raspberry Pi
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)


# Двоичное представление десятичного числа
def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

# Измерение напряжения на выходе troyka-модуля
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

# Вывод двоичного представления в область светодиодов
def outleds(_dec_value):
    GPIO.output(leds, dec2bin(_dec_value))


try:
    # Инициализация переменных
    values = []
    value = 0
    t_begin = time.time()

    # Зарядка конденсатора
    GPIO.output(troyka, 1)
    while (value < 0.93 * 255):
        value = adc()
        values.append(value)
        outleds(value)
    
    # Разрядка конденсатора
    GPIO.output(troyka, 0)
    while (value > 0.02 * 255):
        value = adc()
        values.append(value)
        outleds(value)
    
    # Опредение длительности эксперимента
    t_end = time.time()
    t_length = t_end - t_begin

    # Построение графика
    num_values = len(values)
    plt.plot(range(num_values), values)
    plt.show()

    # Запись данных эксперимента в файл
    value_str = [str(entry) for entry in values]
    with open('data.txt', 'w') as data:
        data.write('\n'.join(value_str))

    # Запись параметров эксперимента в файл
    with open('settings.txt', 'w') as data:
        frequency_str = 'Средняя частота дискретизации:' + '{:.2f}'.format(num_values / t_length) + 'Гц'
        step_str = 'Шаг квантования АЦП:' + '{:.3f}'.format(3.3 / 256) + 'В'
        data.write(frequency_str)
        data.write(step_str)
    
    # Вывод резултатов эксперимента в терминал
    print('Время эксперимента:', '{:.2f}'.format(t_length), 'с')
    print('Период одного измерения:', '{:.2f}'.format(t_length / num_values), 'с')
    print('Средняя частота дискретизации:', '{:.2f}'.format(num_values / t_length), 'Гц')
    print('Шаг квантования АЦП:', '{:.3f}'.format(3.3 / 256), 'В')

finally:
    # Завершение эксперимента
    GPIO.output(dac, 0)
    GPIO.cleanup()