"""
Performs linear regression using native python code.

To run the program enter command:
python native_regression.py <path to data file>

For example:
python native_regression.py chirps.txt

@Module: native_regression.py
@Author: Anna Malmgren
"""

from matrix import *
import matplotlib.pyplot as plt
import sys


def main():
    X, Y = transpose(loadtxt(sys.argv[1]))[:2]
    Xp = powers(X, 0, 1)
    Yp = powers(Y, 1, 1)
    Xpt = transpose(Xp)

    [[b], [m]] = matmul(invert(matmul(Xpt, Xp)), matmul(Xpt, Yp))
    Y2 = [b + m * X[i] for i in range(len(X))]

    plt.plot(X, Y, 'ro')
    plt.plot(X, Y2)
    plt.show()


if __name__ == '__main__':
    main()
