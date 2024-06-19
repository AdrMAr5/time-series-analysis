import pandas as pd
from scipy.spatial.distance import euclidean, minkowski


def load_data(file_path):
    data = pd.read_csv(file_path, header=None, names=['date', 'series1', 'series2'])
    data['date'] = pd.to_datetime(data['date'], format='%d/%m/%y')
    return data


def moving_window_distance(series1, series2, window_size, distance_metric):
    distances = []
    for i in range(len(series1) - window_size + 1):
        window1 = series1[i:i + window_size]
        window2 = series2[i:i + window_size]
        distances.append(distance_metric(window1, window2))
    return distances


def shifted_distance(series1, series2, shift, distance_metric):
    series1_shifted = series1.shift(shift).dropna()
    series2_aligned = series2[:len(series1_shifted)]
    return distance_metric(series1_shifted, series2_aligned)


def segment_distance(series1, series2, num_segments, shift, distance_metric):
    segment_length = len(series1) // num_segments
    distances = []
    for i in range(0, len(series1), segment_length):
        segment1 = series1[i:i + segment_length]
        segment2 = series2[i + shift:i + shift + segment_length]
        if len(segment1) == len(segment2):
            distances.append(distance_metric(segment1, segment2))
    return distances


def calculate_minkowski_param(series1, series2, start_index, p):
    distances = []
    minkowski_p = p
    for i in range(start_index, len(series1)):
        dist_concurrent = minkowski(series1[i:], series2[i:], p=minkowski_p)
        dist_shift_minus = shifted_distance(series1, series2, -int(len(series1) * 0.1),
                                            lambda x, y: minkowski(x, y, p=minkowski_p))
        dist_shift_plus = shifted_distance(series1, series2, int(len(series1) * 0.1),
                                           lambda x, y: minkowski(x, y, p=minkowski_p))

        if dist_shift_minus < dist_concurrent:
            minkowski_p += 1
        elif dist_shift_plus < dist_concurrent and minkowski_p > 1:
            minkowski_p -= 1

        distances.append(dist_concurrent)

    return distances, minkowski_p


def main():
    file_path = 'stock-data.csv'
    data = load_data(file_path)

    # Zadanie 1
    window_size_1_percent = int(len(data) * 0.01)
    window_size_5_percent = int(len(data) * 0.05)

    euclidean_dist_1_percent = moving_window_distance(data['series1'], data['series2'], window_size_1_percent,
                                                      euclidean)
    euclidean_dist_5_percent = moving_window_distance(data['series1'], data['series2'], window_size_5_percent,
                                                      euclidean)

    # Zadanie 2
    shifts = [50, 100, 150]

    euclidean_distances = [shifted_distance(data['series1'], data['series2'], shift, euclidean) for shift in shifts]
    minkowski_distances = [shifted_distance(data['series1'], data['series2'], shift, lambda x, y: minkowski(x, y, p=5))
                           for shift in shifts]

    # Zadanie 3
    shifts_10_percent = [0, int(len(data) * 0.1), -int(len(data) * 0.1)]

    segment_distances = {
        'euclidean': {shift: segment_distance(data['series1'], data['series2'], 10, shift, euclidean) for shift in
                      shifts_10_percent},
        'minkowski': {
            shift: segment_distance(data['series1'], data['series2'], 10, shift, lambda x, y: minkowski(x, y, p=5)) for
            shift in shifts_10_percent}
    }

    # Zadanie 4
    distances, final_minkowski_p = calculate_minkowski_param(data['series1'], data['series2'], 100, p=5)

    print("Zadanie 1:")
    print(f"({len(euclidean_dist_1_percent)} elementow)Odległości Euklidesowe w oknie 1%:", ' '.join(map(str, euclidean_dist_1_percent)))
    print(f"({len(euclidean_dist_5_percent)} elementow)Odległości Euklidesowe w oknie 5%:", ' '.join(map(str, euclidean_dist_5_percent)))

    print("\nZadanie 2:")
    print("Odległości Euklidesowe dla przesunięć:")
    for i in range(len(shifts)):
        print(f"Przesunięcie {shifts[i]}: {euclidean_distances[i]}")
    print("Odległości Minkowskiego dla przesunięć:")
    for i in range(len(shifts)):
        print(f"Przesunięcie {shifts[i]}: {minkowski_distances[i]}")

    print("\nZadanie 3:")
    print("Odległości segmentowe dla różnych przesunięć:")
    print("Odległości Euklidesowe:")
    for shift in segment_distances['euclidean']:
        print(f"({len(segment_distances['euclidean'][shift])} elementow)Przesunięcie {shift}: {' '.join(map(str,segment_distances['euclidean'][shift]))}")
    print("Odległości Minkowskiego:")
    for shift in segment_distances['minkowski']:
        print(f"({len(segment_distances['minkowski'][shift])} elementow)Przesunięcie {shift}: {' '.join(map(str,segment_distances['minkowski'][shift]))}")

    print("\nZadanie 4:")
    print(f"({len(distances)} elementow)Odległości Minkowskiego po modyfikacjach:", ' '.join(map(str, distances)))


if __name__ == "__main__":
    main()
