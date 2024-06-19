import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr


def load_data(filename):
    date_parser = lambda x: pd.to_datetime(x, format='%d/%m/%y')
    data = pd.read_csv(filename, header=None, parse_dates=[0], date_parser=date_parser)
    data.columns = ['Date', 'Series1', 'Series2']
    return data


def select_windows(data, window_length=200, num_windows=5):
    max_start_idx = len(data) - 2 * window_length  # Ensure there is space for both windows
    window_starts = np.random.choice(max_start_idx, num_windows, replace=False)
    windows = [(start, start + window_length) for start in window_starts]
    return windows


def calculate_statistics(data, windows):
    results = []

    for (L1, L2) in windows:
        window1 = data.iloc[L1:L2][['Series1', 'Series2']]
        window2_start = L1 + len(window1)
        window2_end = window2_start + len(window1)
        if window2_end > len(data):
            continue

        window2 = data.iloc[window2_start:window2_end][['Series1', 'Series2']]

        mean1 = window1.mean()
        mean2 = window2.mean()
        diff1 = window1.diff().mean()
        diff2 = window2.diff().mean()
        euc_dist = euclidean(window1.mean(), window2.mean())
        corr1, _ = pearsonr(window1['Series1'].dropna(), window2['Series1'].dropna())
        corr2, _ = pearsonr(window1['Series2'].dropna(), window2['Series2'].dropna())

        result = {
            'window1': (L1, L2),
            'window2': (window2_start, window2_end),
            'mean1': mean1,
            'mean2': mean2,
            'diff1': diff1,
            'diff2': diff2,
            'euclidean_distance': euc_dist,
            'correlation1': corr1,
            'correlation2': corr2
        }
        results.append(result)

    return results


def identify_anomalies(results, threshold=0.1):
    anomalies = []

    for i in range(1, len(results)):
        changes = 0

        result = results[i]
        prev_result = results[i - 1]
        if abs(result['mean1']['Series1'] - result['mean2']['Series1']) / abs(result['mean1']['Series1']) > threshold:
            changes += 1
        if abs(result['mean1']['Series2'] - result['mean2']['Series2']) / abs(result['mean1']['Series2']) > threshold:
            changes += 1
        if abs(result['diff1']['Series1'] - result['diff2']['Series1']) / abs(result['diff1']['Series1']) > threshold:
            changes += 1
        if abs(result['diff1']['Series2'] - result['diff2']['Series2']) / abs(result['diff1']['Series2']) > threshold:
            changes += 1
        if abs(result['euclidean_distance'] - prev_result['euclidean_distance']) / abs(
                prev_result['euclidean_distance']) > threshold:
            changes += 1
        if abs(result['correlation1'] - prev_result['correlation1']) / abs(prev_result['correlation1']) > threshold:
            changes += 1
        if abs(result['correlation2'] - prev_result['correlation2']) / abs(prev_result['correlation2']) > threshold:
            changes += 1

        if changes >= 2:
            anomalies.append((result['window1'], result['window2'], changes))

    return anomalies


def main():
    filename = 'stock-data.csv'
    data = load_data(filename)
    windows = select_windows(data)
    print(windows)
    results = calculate_statistics(data, windows)
    anomalies = identify_anomalies(results)

    for anomaly in anomalies:
        print(f'Anomaly detected between windows {anomaly[0]} and {anomaly[1]} with {anomaly[2]} changes.')


if __name__ == '__main__':
    main()
