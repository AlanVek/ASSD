import numpy as np
import matplotlib.pyplot as plt

NPER = 50
points_per_per = 1000

fi = 57.3e3


def new_expo(NPER):
    x_temp = np.linspace(-1 / fi, 1 / fi, num= points_per_per)

    y_temp = 1 * np.exp(-np.abs(5 * fi * x_temp))

    return np.concatenate((y_temp[x_temp >= 0], np.tile(y_temp, NPER - 1), y_temp[x_temp < 0]))


def new_sine(NPER):
    x_temp = np.linspace(0, 15 / (2 * fi), num= points_per_per)

    y_temp = 1 * np.sin(2 * np.pi * x_temp * fi / 5)

    return np.tile(y_temp, NPER)

t = np.linspace(0, NPER * 15 / (2 * fi), num = points_per_per * NPER)
t2 = np.linspace(0, NPER * 2 / fi, num = points_per_per * NPER)

y = new_expo(NPER)
y2 = new_sine(NPER)


with open('Expo_57,3k.txt', 'wt') as file:
    for ti, yi in zip(t, y):
        file.write(str(ti) + ' ' + str(yi) + '\n')


with open('Sine3_2_57,3k.txt', 'wt') as file:
    for ti, yi in zip(t2, y2):
        file.write(str(ti) + ' ' + str(yi) + '\n')