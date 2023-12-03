import logging
import importlib

completed = [
    "01","02"
]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    for day in completed:
        mod = importlib.import_module("D"+day)
        with open(f"./data/{day}/input","r") as f:
            lines = [l.strip() for l in f.readlines()]
            mod.P1().run(lines)
            mod.P2().run(lines)
