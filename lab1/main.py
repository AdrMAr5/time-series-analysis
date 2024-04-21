import csv
from typing import List


def open_in_out_files(file_in, file_out: str) -> (csv.reader, csv.writer):
    with open(file_in, 'r') as data_in:
        with open(file_out, 'w') as out:
            return csv.reader(data_in), csv.writer(out)


def array_average(arr: List[float]):
    return sum(arr)/len(arr)


def last_valid_interpolation(file_in, file_out: str):
    with open(file_in, 'r') as data_in:
        with open(file_out, 'w') as out:
            file_reader, file_writer = csv.reader(data_in), csv.writer(out)
            last_valid = 0
            for line in file_reader:
                if line[1] == '':
                    file_writer.writerow([line[0], last_valid])
                    continue
                file_writer.writerow(line)
                last_valid = line[1]


def last_10_average_interpolation(file_in, file_out: str):
    with open(file_in, 'r') as data_in:
        with open(file_out, 'w') as out:
            file_reader, file_writer = csv.reader(data_in), csv.writer(out)
            last_10_values = []
            for line in file_reader:
                cur_val = line[1]
                if line[1] == '':
                    cur_val = array_average(last_10_values)
                file_writer.writerow([line[0], cur_val])
                if len(last_10_values) >= 10:
                    del(last_10_values[0])
                last_10_values.append(float(cur_val))


def all_previous_average_interpolation(file_in, file_out: str):
    with open(file_in, 'r') as data_in:
        with open(file_out, 'w') as out:
            file_reader, file_writer = csv.reader(data_in), csv.writer(out)
            values_sum = 0
            count = 0
            for line in file_reader:
                cur_value = line[1]
                if line[1] == '':
                    cur_value = values_sum/count
                file_writer.writerow([line[0], cur_value])
                values_sum += float(cur_value)
                count += 1


def previous_and_next_average_interpolation(file_in, file_out: str):
    with open(file_in, 'r') as data_in:
        with open(file_out, 'w') as out:
            file_reader, file_writer = csv.reader(data_in), csv.writer(out)
            last_valid = 0
            avg = 0
            for index, line in enumerate(file_reader):
                print(index, '1')
                if line[1] == '':
                    file_reader2 = csv.reader(data_in)
                    for index2, line2 in enumerate(file_reader2):
                        print(index2)
                        if index2 > index:
                            print(line2)
                            if line2[1] != '':
                                avg = (last_valid + float(line2[1])) / 2
                                print(avg, last_valid, line2[1])
                                break
                else:
                    last_valid = float(line[1])
                    file_writer.writerow(line)
                    continue
                file_writer.writerow([line[0], avg])


DATA_FILE = 'dane_zad1.csv'

if __name__ == '__main__':
    # last_valid_interpolation(DATA_FILE, 'out_zad1-1.csv')
    last_10_average_interpolation(DATA_FILE, 'out_zad1-2.csv')
    # all_previous_average_interpolation(DATA_FILE, 'out_zad1-3.csv')
    # previous_and_next_average_interpolation(DATA_FILE, 'out_zad1-4.csv')

