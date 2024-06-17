import pandas as pd
from scipy.spatial.distance import euclidean, minkowski

# Wczytanie danych z pliku CSV
data = pd.read_csv('stock-data.csv', header=None, names=['date', 'series1', 'series2'])

# Konwersja daty na format datetime
data['date'] = pd.to_datetime(data['date'], format='%d/%m/%y')


# Funkcja do obliczania odległości w oknie ruchomym
def moving_window_distance(series1, series2, window_size, distance_metric):
    distances = []
    for i in range(len(series1) - window_size + 1):
        window1 = series1[i:i + window_size]
        window2 = series2[i:i + window_size]
        distances.append(distance_metric(window1, window2))
    return distances


# Zadanie 1
window_size_1_percent = int(len(data) * 0.01)
window_size_5_percent = int(len(data) * 0.05)

euclidean_dist_1_percent = moving_window_distance(data['series1'], data['series2'], window_size_1_percent, euclidean)
euclidean_dist_5_percent = moving_window_distance(data['series1'], data['series2'], window_size_5_percent, euclidean)


# Zadanie 2
def shifted_distance(series1, series2, shift, distance_metric):
    series1_shifted = series1.shift(shift).dropna()
    series2_aligned = series2[:len(series1_shifted)]
    return distance_metric(series1_shifted, series2_aligned)


shifts = [50, 100, 150]

euclidean_distances = [shifted_distance(data['series1'], data['series2'], shift, euclidean) for shift in shifts]
minkowski_distances = [shifted_distance(data['series1'], data['series2'], shift, lambda x, y: minkowski(x, y, p=5)) for
                       shift in shifts]


# Zadanie 3
def segment_distance(series1, series2, num_segments, shift, distance_metric):
    segment_length = len(series1) // num_segments
    distances = []
    for i in range(0, len(series1), segment_length):
        segment1 = series1[i:i + segment_length]
        segment2 = series2[i + shift:i + shift + segment_length]
        if len(segment1) == len(segment2):
            distances.append(distance_metric(segment1, segment2))
    return distances


shifts_10_percent = [0, int(len(data) * 0.1), -int(len(data) * 0.1)]

segment_distances = {
    'euclidean': {shift: segment_distance(data['series1'], data['series2'], 10, shift, euclidean) for shift in
                  shifts_10_percent},
    'minkowski': {
        shift: segment_distance(data['series1'], data['series2'], 10, shift, lambda x, y: minkowski(x, y, p=5)) for
        shift in shifts_10_percent}
}

# # Zadanie 4
# Oblicz odległości szeregów (współbieżnie) z wykorzystaniem miary Minkowskiego (z parametrem 5). Począwszy
# od 100. próbki, jeśli odległość szeregów z przesunięciem -10% jest mniejsza niż odległość liczona współbieżnie,
# zmień parametr miary Minkowskiego o +1. Jeśli odległość szeregów z przesunięciem +10% jest mniejsza niż
# odległość liczona współbieżnie, zmień parametr miary Minkowskiego o –1

distances = []
minkowski_param = 5
for i in range(100, len(data)):
    distance_concurrent = minkowski(data['series1'][i:], data['series2'][i:], p=minkowski_param)
    distance_shifted_minus_10 = shifted_distance(data['series1'], data['series2'], -int(len(data) * 0.1), lambda x, y: minkowski(x, y, p=minkowski_param))
    distance_shifted_plus_10 = shifted_distance(data['series1'], data['series2'], int(len(data) * 0.1), lambda x, y: minkowski(x, y, p=minkowski_param))

    if distance_shifted_minus_10 < distance_concurrent:
        minkowski_param += 1
    elif distance_shifted_plus_10 < distance_concurrent and minkowski_param > 1:
        minkowski_param -= 1

    distances.append(distance_concurrent)


# Wyświetlenie wyników
print("Zadanie 1:")
print("Odległości Euklidesowe w oknie 1%:", ' '.join(map(str, euclidean_dist_1_percent)))
print("Odległości Euklidesowe w oknie 5%:", ' '.join(map(str, euclidean_dist_5_percent)))

print("\nZadanie 2:")
print("Odległości Euklidesowe dla przesunięć:")
# print the table of distances
for i in range(len(shifts)):
    print(f"Przesunięcie {shifts[i]}: {euclidean_distances[i]}")
print("Odległości Minkowskiego dla przesunięć:", minkowski_distances)
for i in range(len(shifts)):
    print(f"Przesunięcie {shifts[i]}: {minkowski_distances[i]}")

print("\nZadanie 3:")
print("Odległości segmentowe dla różnych przesunięć:", segment_distances)

print("\nZadanie 4:")
print("Odległości Minkowskiego po modyfikacjach:", distances)
