#!/usr/bin/env python3
import sys
import logging

class P1:
    def __init__(self):
        self.log = logging.getLogger(":".join([__file__,type(self).__name__]))

    def run(self, lines:list):
        pass

class P2(P1):
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1],"r") as f:
        lines = [l.strip() for l in f.readlines()]
    P1().run(lines)
    P2().run(lines)