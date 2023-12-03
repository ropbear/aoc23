#!/usr/bin/env python3
import sys
import logging

class DXXP1:
    def __init__(self):
        pass

    def run(self, lines:list):
        pass

class DXXP2(DXXP1):
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1],"r") as f:
        lines = [l.strip() for l in f.readlines()]
    DXXP1().run(lines)
    DXXP2().run(lines)