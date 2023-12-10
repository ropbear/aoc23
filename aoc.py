import time
import logging
import importlib

completed = [
    "01","02","03","04"
]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    for day in completed:
        mod = importlib.import_module("D"+day)
        with open(f"./data/{day}/input","r") as f:
            lines = [l.strip() for l in f.readlines()]
            start = time.time()
            mod.P1().run(lines)
            logging.info(f"Runtime D{day}.P1: {time.time()-start:4.3f}s")
            start = time.time()
            mod.P2().run(lines)
            logging.info(f"Runtime D{day}.P2: {time.time()-start:4.3f}")
