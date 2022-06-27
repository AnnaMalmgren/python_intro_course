"""
Module containing functions for common matrix computations
@Module: matrix.py
@Author: Anna Malmgren
"""


def transpose(m):
    """
    Transposes given matrix m and returns the transposed matrix.
    """
    return [list(row) for row in zip(*m)]


def powers(list, start, end):
    """
    Computes and returns a matrix by, for each number in the given list,
    create a row containing the powers of the number using the range from
    given start- to given end number.
    """
    return [[pow(num, i) for i in range(start, (end + 1))] for num in list]


def matmul(m_a, m_b):
    """
    Multiplies two given matrices, m_a and m_b, and returns the product matrix.
    If any of the given matrices is empty or if the columns in m_a doesn't have
    the same length as the rows in m_b the function returns an empty list
    """
    if not m_a or (len(m_a[0]) != len(m_b)):
        return []

    a_rows, b_cols, b_rows = len(m_a), len(m_b[0]), len(m_b)
    matrix = [[0] * b_cols for i in range(a_rows)]

    for n in range(a_rows):
        for m in range(b_cols):
            for k in range(b_rows):
                matrix[n][m] += m_a[n][k] * m_b[k][m]

    return matrix


def invert(m):
    """
    Creates an inverted matrix using the given matrix m. The function only
    allows square matrices with a length of 2, if a matrix with wrong format
    is given, an empty list is returned otherwise the inverted matrix.
    """
    if (len(m) != len(m[0])) or len(m) != 2:
        return []

    det = (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])

    return [[(m[1][1] / det), (- 1 * m[0][1] / det)],
            [(-1 * m[1][0] / det), (m[0][0] / det)]]


def loadtxt(file_name):
    """
    Converts content of the file with given file_name to a matrix of
    numbers, where every file line converts to a row.
    The file should contain numbers that are seperated by white spaces
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        numbers = [[float(i) for i in line.split()] for line in file]
        file.close()
        return numbers
