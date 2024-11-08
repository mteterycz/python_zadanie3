import argparse
import os
import json
import random


def save_to_file(file_name):
    
    data = [
        {
            "Model": random.choice(["A", "B", "C"]),
            "Wynik": random.randint(0, 1000),
            "Czas": f"{random.randint(0, 1000)}s",
        }
    ]

    with open(file_name, "w") as file:
        json.dump(data, file, indent=1)


def read_file(file_name_list):
    
    sum = 0

    for file_name in file_name_list:
        with open(file_name, "r") as fh:
            data = json.load(fh)
            for object in data:
                sum += int(object["Czas"][:-1])
    return sum


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--months",
        type=str,
        nargs="+",
        required=True,
        help="Lista miesięcy (format: m1 m2 ... mn)",
    )
    parser.add_argument(
        "-d", "--days",
        type=str,
        nargs="+",
        required=True,
        help="Lista zakresow dni tygodnia "
             "(format: d11-d12-...-d1p ... dn1-dn2-...-dnq)",
    )
    parser.add_argument(
        "-t", "--times",
        type=str,
        nargs="*",
        help="Pora dnia (format: t1 t2 ...)"
    )
    parser.add_argument(
        "-c", "--create",
        action="store_true",
        help="Tworzenie plikow (domyslnie odczytywanie)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if len(args.months) != len(args.days):
        print("Liczba miesiecy musi byc rowna liczbie zakresow dni tygodnia")
        return

    if args.create:
        print("Tworzenie plikow")
        cwd = os.getcwd()
        t = 0
        for i in range(len(args.months)):
            days = args.days[i].split("-")
            for day in days:
                if t >= len(args.times):
                    path = os.path.join(cwd, args.months[i], day, "r")
                else:
                    path = os.path.join(cwd, args.months[i], day, args.times[t])
                    t += 1

                os.makedirs(path, exist_ok=True)
                save_to_file(os.path.join(path, "Dane.json"))
        print("Zakonczono tworzenie plikow")

    else:
        print("Odczytywanie plikow")
        cwd = os.getcwd()
        t = 0
        files = []
        for i in range(len(args.months)):
            days = args.days[i].split("-")
            for day in days:
                if t >= len(args.times):
                    path = os.path.join(cwd, args.months[i], day, "r", "Dane.json")
                else:
                    path = os.path.join(
                        cwd, args.months[i], day, args.times[t], "Dane.json"
                    )
                t += 1
                files.append(path)

        sum = read_file(files)

        print("Zakonczono odczytywanie plikow\nSuma =", sum)


if __name__ == "__main__":
    main()
