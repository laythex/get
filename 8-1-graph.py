import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Чтение параметров измерений
with open("settings.txt", "r") as f:
    freq, step = [float(i) for i in f.read().split('\n')]

# Чтение значений измерений
data = np.loadtxt("data.txt")
data *= step

# Вычисление параметров измерений
N = data.size
dt = 1 / freq

# Создание требуемого временного диапазона
time_range = np.arange(0, dt * N, dt)

# Поиск минимального и максимального значений
max_arg = np.argmax(data)
min_arg = N - 1

# Вычисление времени заряда и разряда
charge_time = max_arg * dt
discharge_time = (min_arg - max_arg) * dt 

# Создание фигуры
fig, ax = plt.subplots(figsize=(12, 7))

# Отрисовка графика
ax.plot(time_range, data, 'bo-', linewidth=0.75, markersize=4, markevery=340)

# Работа с осями
ax.set_title('Процесс заряда и разряда конденсатора в RC-цепочке')
ax.set_xlabel('Время, с')
ax.set_ylabel('Напряжение, В')

ax.set_xlim(0, 80)
ax.set_ylim(0, 3.5)

ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

# Добавление сетки
ax.grid(which='major')
ax.grid(which='minor', linewidth=0.4, linestyle='--')

# Добавление легенды
ax.legend(['V(t)'])

# Добавление аннотаций
ax.text(42.5, 2.82, 'Время заряда = ' + '{:.2f}'.format(charge_time) + ' с')
ax.text(42.5, 2.62, 'Время разряда = ' + '{:.2f}'.format(discharge_time) + ' с')

# Сохранение графика и вывод его на экран
plt.savefig('8-1-graph.svg')
plt.show()
