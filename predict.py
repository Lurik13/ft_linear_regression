from linear_regression import OUTFILE_NAME, estimatePrice


if __name__ == '__main__':
    try:
        with open(OUTFILE_NAME, 'r') as paramsFile:
            theta0, theta1 = paramsFile.readline().split(', ')
            mileage = input('Enter a mileage: ')
            print(estimatePrice(float(theta0), float(theta1), int(mileage)))
    except:
        print("\033[38;2;170;0;0;1;4mVous devez d'abord executer la premiere partie du programme.")
