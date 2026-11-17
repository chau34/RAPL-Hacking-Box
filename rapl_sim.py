import sys
import csv
import time
import random
import socket
import threading
import os

host = "localhost"
port = 8932

def noise(level):
    if (level == "medium"):
        return random.gauss(0, 0.5)
    if (level == "hard"):
        return random.gauss(0, 1)
    # level easy or default
    return random.gauss(0, 0.2)

def listen_for_workload(getting_work):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while (True):
            conn, _ = s.accept()
            with conn:
                message = conn.recv(1024).decode()
                if (message == "1"):
                    getting_work.set()
                    print("comparing!")
                else:
                    getting_work.clear()
                    print("done!")
                
def main(args):
    getting_work = threading.Event()

    listener = threading.Thread(
        target=listen_for_workload,
        args=(getting_work,),
        daemon=True
    )
    listener.start()

    power_base = 10.0
    power_compare = 5.0

    energy = 5000
    time_stamp = 0
    prev = time.monotonic()

    with open("energy_readings.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "energy"])

    while(True):
        time.sleep(0.1)

        power_work = power_compare if getting_work.is_set() else 0.0

        now = time.monotonic()
        time_diff = now - prev
        prev = now

        power = power_base + power_work
        energy += power * time_diff
        measured_energy = energy + noise(args[1])
        
        time_stamp += 1
        new_row = [time_stamp, measured_energy]

        with open("energy_readings.csv", 'r', newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))

        # only keep last 100 readings
        if len(rows) >= 100:
            rows = rows[:100]

        # insert after the header
        rows.insert(1, new_row)

        # overwrite the file with the updated list
        with open("energy_readings.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

if __name__ == "__main__":
    # defaults to easy mode
    args = [sys.argv[0], "easy"]
    # change mode if given
    if (len(sys.argv) == 2):
        args[1] = sys.argv[1]
    main(args)