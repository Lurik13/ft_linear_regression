# import matplotlib
# matplotlib.use('Agg') # Anti-Grain Geometry

import sys
import time
from prompt_toolkit import prompt
from input import AccentInsensitiveCompleter, normalize
import matplotlib.pyplot as plt
import numpy as np

OUTFILE_NAME = "params.csv"


def parseData(fileName):
    linesNumber = 0
    xValues = []
    yValues = []
    with open(fileName) as f:
        plt.title((fileName[:-4]))
        for line in f:
            values = line[:-1].split(",")  # removes '\n' before splitting
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


def normalizeValues(x, y):
    x_max, y_max = max(x), max(y)
    x = [val / x_max for val in x]
    y = [val / y_max for val in y]
    return x, y


def displayFigure(x, y):
    responses = ['Yes', 'No']
    completer = AccentInsensitiveCompleter(responses)
    new_prompt = prompt(
        'Would you like to see the real data? ([Yes], No)\n',  # a revoir
        completer=completer, complete_while_typing=True
    )
    if (not normalize(new_prompt) in 'Yes'):
        x, y = normalizeValues(x, y)
    plt.scatter(x, y)
    regression_line, = plt.plot(
        [], [],
        color='LightCoral',
        label='Regression Line'
    )
    x_min, x_max = min(x), max(x)
    y_min = estimatePrice(x_min, 0.657577, 0.170032)
    y_max = estimatePrice(x_max, 0.657577, 0.170032)
    regression_line.set_data([x_min, x_max], [y_min, y_max])
    plt.show()


def estimatePrice(theta0, theta1, mileage):
    return theta0 + (theta1 * mileage)


def ft_linear_regression(x, y):
    theta0 = 0
    theta1 = 0
    iterations = 300
    learningRate = 0.01
    m = len(x)
    for iteration in range(iterations):
        sum_error_theta0 = 0
        sum_error_theta1 = 0
        for i in range(m):
            predictedPrice = estimatePrice(theta0, theta1, x[i])
            error = predictedPrice - y[i]
            # print("\033[38;2;0;170;0m", error, predictedPrice)
            sum_error_theta0 += error
            sum_error_theta1 += error * x[i]
        print(f'\033[38;2;170;0;0m{sum_error_theta0}, {sum_error_theta1}\033[0m')
        theta0 -= learningRate / m * sum_error_theta0
        theta1 -= learningRate / m * sum_error_theta1
        print(f"Iteration {iteration}; Theta0 {theta0:.6f}; Theta1 {theta1:.6f}")
    return theta0, theta1


def saveParams(theta0, theta1):
    with open(OUTFILE_NAME, 'w') as outfile:
        outfile.write(f"{theta0}, {theta1}")


def standardize(feature):
    mean = np.mean(feature)
    std = np.std(feature)
    return [(v - mean) / std for v in feature], mean, std


def unstandardize(theta0, theta1, x_mean, x_std, y_mean, y_std):
    slope = theta1 * (y_std / x_std)
    intercept = y_std * theta0 + y_mean - slope * x_mean
    return intercept, slope


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception("Please fill in a data file.")
        x, y = parseData(sys.argv[1])
        # displayFigure(x, y)
        # normalizedX, normalizedY = normalizeValues(x, y)
        x, x_mean, x_std = standardize(x)
        y, y_mean, y_std = standardize(y)
        theta0, theta1 = ft_linear_regression(x, y)
        theta0, theta1 = unstandardize(theta0, theta1, x_mean, x_std, y_mean, y_std)
        saveParams(theta0, theta1)

    except Exception as e:
        print("\033[38;2;170;0;0;1;4m" + str(e) + "\033[0m")
