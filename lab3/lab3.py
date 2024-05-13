from lab2.main import minkowski_przedzialy_transform, transform_pow


def zad1():
    print('euklides / minkowski dla m=2: ')
    minkowski_przedzialy_transform('stock-data.csv', [125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1258], transform_pow(1), m=2, data_start_col=1, data_end_col=2)
    print('minkowski dla m=5: ')
    minkowski_przedzialy_transform('stock-data.csv', [125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1258], transform_pow(1), m=5, data_start_col=1, data_end_col=2)


def main():
    zad1()


if __name__ == "__main__":
    main()
