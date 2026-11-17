import csv
import pandas as pd

def analyze(sample_count=50):
    with open("energy_readings.csv", 'r', newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))[1:sample_count + 1]

    energy_changes = []

    for latest, earliest in zip(rows, rows[1:]):
        energy_changes.append(float(latest[1]) - float(earliest[1]))

    average = sum(energy_changes) / len(energy_changes)
    print("Samples analyzed:", len(energy_changes))
    print("Average energy change:", average)

    df = pd.DataFrame({"values": energy_changes})
    df["rolling_mean"] = df["values"].rolling(window=10).mean()

    highest = df["rolling_mean"].max()
    highest_idx = df["rolling_mean"].idxmax()

    print("Highest rolling average:", highest)
    print("Window ending at index:", highest_idx)


if __name__ == "__main__":
    analyze()
