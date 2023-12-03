#!/usr/bin/env python3
import sys
import logging

isdigit = lambda x: 0 < (ord(x)-0x30) < 10

wordmap = {
    "one":'1',
    "two":'2',
    "three":'3',
    "four":'4',
    "five":'5',
    "six":'6',
    "seven":'7',
    "eight":'8',
    "nine":'9'
}

class P1:
    def __init__(self, level=logging.INFO):
        self.log = logging.getLogger(":".join([__file__,type(self).__name__]))

    def count_digits(self, line:str) -> int:
        num = 0
        for c in line:
            num += 1 if isdigit(c) else 0
        return num

    def get_first_digit(self, line:str) -> int:
        for c in line:
            if isdigit(c):
                return c
        return None

    def get_calibration_value(self, line:str) -> int:
        num_digits = self.count_digits(line)
        left = self.get_first_digit(line)
        right = self.get_first_digit(line[::-1])

        if num_digits == 0:
            return 0
        else:
            return int(left+right)

    def run(self, lines:list):
        ans = sum([self.get_calibration_value(l) for l in lines])
        self.log.info(f"ans: {ans}")
        return ans

class P2(P1):
    def lookahead(self, chars:str) -> str:
        for word in wordmap.keys():
            if chars[0:len(word)] == word:
                return word
        return None

    def words2int(self, line:str) -> str:
        builder = ['']*len(line)
        skipping = None
        skiplen = 0
        for i in range(len(line)):
            if skiplen == 0:
                skipping = False
            word = self.lookahead(line[i:])
            if word is not None:
                builder[i] = wordmap[word]
                skipping = True
                skiplen = len(word) - 1 # the most two numwords can share is 1 char
            elif not skipping:
                builder[i] = line[i]
            else:
                skiplen -= 1
                
        return ''.join(builder)

    def run(self, lines:list):
        ans = sum([self.get_calibration_value(self.words2int(l)) for l in lines])
        self.log.info(f"ans: {ans}")
        return ans


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1],"r") as f:
        lines = [l.strip() for l in f.readlines()]
    P1().run(lines)
    P2().run(lines)