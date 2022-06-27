"""
Module: topmost.py
Author: Anna Malmgren
Version: 1.0

Tokenizes texts into words, calculates and prints top most words
and calculates and prints cosine similarity between two texts, using
given command line arguments
"""
import sys
import urllib.request
import wordfreq as wf

# Constants
HTTP, HTTPS = ('http', 'https')
UTF8, NEW_LINE = 'utf-8', '\n'
STOP_WORDS, TEXT, N, COMPARE_FILE = 1, 2, 3, 4
MIN_ARGV_LEN = 4
ERR_MSG_ARGV_LEN = ('Incorrect number of arguments, provide minimum:\nPath to '
                    'stop words, Path to text, Number of words to print')
ERR_MSG_INT = 'Number of words to be printed (argv[3]) must be a number'
ERR_MSG_FILE = 'The given file: "{}" could not be found'
ERR_MSG = "Sorry, something went wrong"


def main():
    """
    Runs the application using provided commandline arguments.
    Commandline arguments should be:
    <path_stopwords> <path_text> <topmost_number> <path_comparefiles>(optional)
    """
    if not checkArguments():
        return

    pathStop, pathText, n = sys.argv[1:MIN_ARGV_LEN]
    words, stopWords = getWords(pathText), getStopWords(pathStop)
    topMost = wf.countWords(words, stopWords)

    wf.printTopMost(topMost, n)

    # if compare file/files (sys.argv[5] and more) is given, compute and print
    # cosine similarity
    if len(sys.argv) > MIN_ARGV_LEN:
        compareFiles = sys.argv[COMPARE_FILE:]
        for file in compareFiles:
            wordsB = getWords(file)
            print(NEW_LINE + sys.argv[TEXT] + ', ' + file)
            wf.printCosineSimularity(topMost, wf.countWords(wordsB, stopWords))


def checkArguments() -> bool:
    return correctArgvLen(sys.argv) and argIsDigit(sys.argv)


def correctArgvLen(arg: list) -> bool:
    isCorrectLen = len(arg) >= MIN_ARGV_LEN
    if not isCorrectLen:
        print(ERR_MSG_ARGV_LEN)

    return isCorrectLen


def argIsDigit(arg: list) -> bool:
    isDigit = arg[N].isdigit()
    if not isDigit:
        print(ERR_MSG_INT)

    return isDigit


def getWords(path: str) -> list:
    words = []

    if isURL(path):
        response = urllib.request.urlopen(path)
        words = wf.tokenize(response.read().decode(UTF8).splitlines())
    else:
        with open(path, encoding=UTF8) as file:
            words = wf.tokenize(file)
            file.close()

    return words


def isURL(str: str) -> bool:
    return str.startswith(HTTP) or str.startswith(HTTPS)


def getStopWords(path: str) -> list:
    with open(path, encoding=UTF8) as file:
        stopWords = [line.strip(NEW_LINE) for line in file]
        file.close()
    return stopWords


if __name__ == '__main__':
    try:
        main()

    except FileNotFoundError as e:
        print(ERR_MSG_FILE.format(e.filename))
    except Exception:
        print(ERR_MSG)
