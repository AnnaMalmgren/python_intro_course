"""
Module: wordfreq.py
Author: Anna Malmgren
Version: 1.0

Contains functions for tokenize texts, count words,
print and plot Topmost words, calculate and print cosine simularity
"""

import matplotlib.pyplot as plt
import math


def tokenize(lines: str) -> list:
    words = []

    for line in lines:
        extractWords(words, line)

    return words


def extractWords(words: list, line: str) -> None:
    start, end = 0, 0

    while start < len(line):
        start = removeSpaces(line, start)

        if start == len(line):
            break
        else:
            end = getWordEnd(line, start)

        appendWord(words, line[start:end])
        start = end


def removeSpaces(line: str, start: int) -> int:
    while start < len(line) and line[start].isspace():
        start += 1
    return start


def getWordEnd(line: str, start: int) -> int:
    end = start

    if line[start].isdigit():
        while end < len(line) and line[end].isdigit():
            end += 1
    elif line[start].isalpha():
        while end < len(line) and line[end].isalpha():
            end += 1
    else:
        end += 1

    return end


def appendWord(words: list, word: str) -> None:
    words.append(word.lower() if word.isalpha() else word)


def countWords(words: list, stopWords: list) -> dict:
    wordCount = {}
    initialCount = 0

    for word in words:
        if word not in stopWords:
            wordCount[word] = wordCount.get(word, initialCount) + 1

    return wordCount


def printTopMost(frequencies: dict, n: int) -> None:
    left, right = 20, 5
    topMost = getTopMost(frequencies, n)

    for (word, count) in topMost:
        print(str(word).ljust(left) + str(count).rjust(right))


def getTopMost(freq: dict, i: int) -> list:
    index = 1
    return sorted(freq.items(), key=lambda x: -x[index])[:int(i)]


# Testing Zipf functionality
def Zipf(frequencies: dict, n: int) -> None:
    ranks, counts = [], []
    topMost = getTopMost(frequencies, n)

    for i, (word, count) in enumerate(topMost):
        ranks.append(i + 1)
        counts.append(count)

    Y1 = [counts[0]/rank for rank in ranks]
    plt.plot(ranks, counts, 'ro')
    plt.plot(ranks, Y1)
    plt.show()


# Testing cosine simularity
def printCosineSimularity(wordsA: dict, wordsB: dict) -> None:
    print('Cosine simularity: ' + str(getCosineSimularity(wordsA, wordsB)))


def getCosineSimularity(dictA: dict, dictB: dict) -> float:
    vectA, vectB = getVects(dictA, dictB)

    numerator = dotProduct(vectA, vectB)

    denominator = (math.sqrt(dotProduct(vectA, vectA)) *
                   math.sqrt(dotProduct(vectB, vectB)))

    return numerator / denominator


def getVects(dictA: dict, dictB: dict) -> tuple:
    same = set(dictA.keys()).intersection(dictB.keys())
    vectA, vectB = [], []

    for i in same:
        vectA.append(int(dictA[i]))
        vectB.append(int(dictB[i]))

    return vectA, vectB


def dotProduct(vectA: list, vectB: list) -> int:
    return sum(a * b for a, b in zip(vectA, vectB))
