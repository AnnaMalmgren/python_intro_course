"""
Performs polynomial regression using numpy.

To run the program enter command:
python numpy_regression.py <path to data file> <degree of the polynomial>

For example:
python numpy_regression.py dataset3.txt 4

@Module: numpy_regression.py
@Author: Anna Malmgren
"""

import numpy as np
from matrix import powers
import matplotlib.pyplot as plt
import sys


def poly(a, x):
    """
    Computes and returns the value of the polynomial using the given list, a,
    containing koefficients and the given value x
    """
    return sum([a[i] * pow(x, i) for i in range(len(a))])


def main():
    filename, degree = sys.argv[1], int(sys.argv[2])
    X, Y = np.transpose(np.loadtxt(filename))[:2]
    Xp = powers(X, 0, degree)
    Yp = powers(Y, 1, 1)
    Xpt = np.transpose(Xp)

    a = np.matmul(np.linalg.inv(np.matmul(Xpt, Xp)), np.matmul(Xpt, Yp))
    a = a[:, 0]

    X2 = np.linspace(min(X), max(X), int((max(X) - min(X)) / 0.2)).tolist()
    Y2 = [poly(a, x) for x in X2]

    plt.plot(X, Y, 'ro')
    plt.plot(X2, Y2)
    plt.show()


if __name__ == '__main__':
    main()
