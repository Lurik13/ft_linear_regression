# import matplotlib
# matplotlib.use('Agg') # Anti-Grain Geometry

import sys
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
            values = line[:-1].split(",")
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

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception("Please fill in a data file.")
        values = parseData(sys.argv[1])
        x = values[0]
        y = values[1]
        print(stats.linregress(x, y))
        slope, intercept, r, p, std_err = stats.linregress(x, y)
        def myfunc(x):
            return slope * x + intercept
        mymodel = list(map(myfunc, x))
        plt.scatter(x, y)
        plt.plot(x, mymodel)
        # plt.savefig(CHART_IMAGE_NAME)
        plt.show()
        print("You can check \033[4m" + CHART_IMAGE_NAME + "\033[0m.")
    except Exception as e:
        print("\033[38;2;170;0;0;1;4m" + str(e) + "\033[0m")
