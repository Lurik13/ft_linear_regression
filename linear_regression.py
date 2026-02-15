import sys
import time
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
            sum_error_theta0 += error
            sum_error_theta1 += error * x[i]
        theta0 -= learningRate / m * sum_error_theta0
        theta1 -= learningRate / m * sum_error_theta1
        print(f"Iteration {iteration}; Theta0 {theta0:.6f}; Theta1 {theta1:.6f}")
    return theta0, theta1


def standardize(axis):
    mean = np.mean(axis)
    std = np.std(axis)
    return [(v - mean) / std for v in axis], mean, std


def unstandardize(theta0, theta1, x_mean, x_std, y_mean, y_std):
    slope = theta1 * (y_std / x_std)
    intercept = y_std * theta0 + y_mean - slope * x_mean
    return intercept, slope


def displayFigure(x, y, intercept, slope):
    plt.scatter(x, y)
    plt.axline(
        (0, intercept), 
        slope=slope, 
        color='LightCoral', 
        label='Regression Line'
    )
    plt.show()


def saveParams(theta0, theta1):
    with open(OUTFILE_NAME, 'w') as outfile:
        outfile.write(f"{theta0}, {theta1}")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception("Please fill in a data file.")
        x, y = parseData(sys.argv[1])
        x_s, x_mean, x_std = standardize(x)
        y_s, y_mean, y_std = standardize(y)
        theta0_s, theta1_s = ft_linear_regression(x_s, y_s)
        theta0, theta1 = unstandardize(theta0_s, theta1_s, x_mean, x_std, y_mean, y_std)
        print(f"\033[38;2;0;170;0mTheta0 {theta0:.6f}; Theta1 {theta1:.6f}\033[0m")
        displayFigure(x, y, theta0, theta1)
        saveParams(theta0, theta1)

    except Exception as e:
        print("\033[38;2;170;0;0;1;4m" + str(e) + "\033[0m")
