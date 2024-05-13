import csv
from typing import List, Callable


def euklides(file_in: str):
    with open(file_in, 'r') as file_in:
        csv_reader = csv.reader(file_in)
        squares_sum = 0
        for line in csv_reader:
            squares_sum += pow(float(line[0]) - float(line[1]), 2)
        print('miara euklidesowska: ', pow(squares_sum, 0.5))


def minkowski(file_in: str, m: int):
    with open(file_in, 'r') as file_in:
        csv_reader = csv.reader(file_in)
        powers_sum = 0
        for line in csv_reader:
            powers_sum += pow(abs(float(line[0]) - float(line[1])), m)
        print(f'minkowski dla m={m}: ', pow(powers_sum, 1/m))


def rmse(file_in: str):
    with open(file_in, 'r') as file_in:
        csv_reader = csv.reader(file_in)
        squares_sum = 0
        lines_count = 0
        for line in csv_reader:
            squares_sum += pow(float(line[0]) - float(line[1]), 2)
            lines_count += 1
        print('RMSE: ', squares_sum/lines_count)


# by default m=2
def minkowski_przedzialy_transform(file_in: str, breakpoints: List[int], transform_fn: Callable[[float], float], m=2, data_start_col=0, data_end_col=1):
    with open(file_in, 'r') as file_in:
        csv_reader = csv.reader(file_in)
        breakpoints.sort()
        next_stop = breakpoints[0]
        last_stop = 1
        powers_sum = 0
        for index, line in enumerate(csv_reader):
            if index == next_stop:
                print(f'minkowski dla m={m} od {last_stop} rekordu do {next_stop} rekordu: ', pow(powers_sum, 1 / m))
                del breakpoints[0]
                last_stop = next_stop + 1
                next_stop = breakpoints[0]
                powers_sum = 0

            transformed_values = [transform_fn(float(item)) for item in line[data_start_col:data_end_col+1]]
            powers_sum += pow(abs(transformed_values[0] - transformed_values[1]), m)

        print(f'minkowski dla m={m} od {last_stop} rekordu do konca: ', pow(powers_sum, 1 / m))


# tworzy nowy plik wynikowy
# liczy średnią dopiero od od k-tego elementu, zatem ostatnie 10 wierszy jest prognozą
def moving_average1(file_in, file_out: str, k: int):
    with open(file_in, 'r') as file_in:
        with open(file_out, 'w') as file_out:
            file_reader, file_writer = csv.reader(file_in), csv.writer(file_out)
            last_k_values = {0: [], 1: []}
            for line in file_reader:
                line = list(map(float, line))
                averages = []
                for col_index, col_val in enumerate(line):
                    last_k_values[col_index].append(col_val)
                    if len(last_k_values[col_index]) < k:
                        continue
                    if len(last_k_values[col_index]) > k:
                        del last_k_values[col_index][0]
                    averages.append(sum(last_k_values[col_index]) / len(last_k_values[col_index]))
                if averages:
                    file_writer.writerow(averages)
            for i in range(k-1):
                for col_index, col_val in enumerate(line):
                    last_k_values[col_index].append(sum(last_k_values[col_index]) / len(last_k_values[col_index]))
                    del last_k_values[col_index][0]
                file_writer.writerow([last_k_values[0][-1], last_k_values[1][-1]])


# tworzy nowy plik wynikowy
# liczy średnią już od pierwszego wiersza czyli pierwszy wiersz jest identyczny jak w pliku wejściowym
def moving_average2(file_in, file_out: str, k: int):
    with open(file_in, 'r') as file_in:
        with open(file_out, 'w') as file_out:
            file_reader, file_writer = csv.reader(file_in), csv.writer(file_out)
            last_k_values = {0: [], 1: []}
            for line in file_reader:
                line = list(map(float, line))
                averages = []
                for col_index, col_val in enumerate(line):
                    last_k_values[col_index].append(col_val)
                    if len(last_k_values[col_index]) > k:
                        del last_k_values[col_index][0]
                    averages.append(sum(last_k_values[col_index]) / len(last_k_values[col_index]))
                if averages:
                    file_writer.writerow(averages)



def transform_pow(exp):
    def inner(value):
        return pow(value, exp)
    return inner


def zadanie_1():
    print('ZADANIE 1:')
    euklides('dane_zad2.csv')
    minkowski('dane_zad2.csv', 2)
    minkowski('dane_zad2.csv', 5)
    rmse('dane_zad2.csv')
    print('---------------')


def zadanie_2():
    print('ZADANIE 2:')
    minkowski_przedzialy_transform('dane_zad2.csv', [300, 800, 1000], transform_pow(1), 2)
    print('---------------')


def zadanie_3():
    print('ZADANIE 3:')
    print('transformacja potęgująca dla wykładnika 3: ')
    minkowski_przedzialy_transform('dane_zad2.csv', [300, 800, 1000], transform_pow(3), 2)
    print('transformacja potęgująca dla wykładnika 4: ')
    minkowski_przedzialy_transform('dane_zad2.csv', [300, 800, 1000], transform_pow(4), 2)
    print('---------------')


def zadanie_4():
    print('ZADANIE 4:')
    # moving_average1 liczy średnią dopiero od od k-tego elementu, zatem ostatnie 10 wierszy jest prognozą
    print('moving average dla k=10: ')
    moving_average1('dane_zad2.csv', 'srednia_ruchoma10_v1.csv', 10)
    minkowski_przedzialy_transform('srednia_ruchoma10_v1.csv', [300, 800, 1000], transform_pow(1), 2)

    # moving_average2 liczy średnią już od pierwszego wiersza czyli pierwszy wiersz jest identyczny jak w pliku
    # wejściowym
    # moving_average2('dane_zad2.csv', 'srednia_ruchoma10_v2.csv', 10)
    print('moving average dla k=40: ')
    moving_average1('dane_zad2.csv', 'srednia_ruchoma40_v1.csv', 40)
    minkowski_przedzialy_transform('srednia_ruchoma40_v1.csv', [300, 800, 1000], transform_pow(1), 2)
    print('---------------')


if __name__ == '__main__':
    zadanie_1()
    zadanie_2()
    zadanie_3()
    zadanie_4()
