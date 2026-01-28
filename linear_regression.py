# import matplotlib
# matplotlib.use('Agg') # Anti-Grain Geometry

import sys
from prompt_toolkit import prompt
from input import AccentInsensitiveCompleter, normalize
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

CHART_IMAGE_NAME = "ft_linear_regression.png"


def parseData(fileName):
    linesNumber = 0
    xValues = []
    yValues = []
    with open(fileName) as f:
        plt.title((fileName[:-4]))
        for line in f:
            values = line[:-1].split(",") # removes '\n' before splitting
            if len(values) != 2:
                raise Exception("Wrong data format.")
            if linesNumber == 0:
                plt.xlabel(values[0])
                plt.ylabel(values[1])
            else:
                xValues.append(int(values[0]))
                yValues.append(int(values[1]))
            linesNumber += 1
        if linesNumber < 2:
            raise Exception("Not enough data.")
    return xValues, yValues

def displayFigure(x, y):
    responses = ['Yes', 'No']
    completer = AccentInsensitiveCompleter(responses)
    new_prompt = prompt('Would you like to see the real data? ([Yes], No)\n', completer=completer, complete_while_typing=True)
    if (not normalize(new_prompt) in 'yes'):
        x_max, y_max = max(x), max(y)
        x = [val / x_max for val in x]
        y = [val / y_max for val in y]
    plt.scatter(x, y)
    plt.show()

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception("Please fill in a data file.")
        x, y = parseData(sys.argv[1])
        displayFigure(x, y)

    except Exception as e:
        print("\033[38;2;170;0;0;1;4m" + str(e) + "\033[0m")
