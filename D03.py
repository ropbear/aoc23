#!/usr/bin/env python3
import sys
import logging
from string import punctuation

isdigit = lambda x: 0 <= (ord(x)-0x30) < 10
SYMBOLS = punctuation.replace('.','')
NONSYM  = 'nonsym'
sys.setrecursionlimit(100000)

class P1:
    def __init__(self):
        self.log = logging.getLogger(":".join([__file__,type(self).__name__]))
        self.matrix = None
        self.nums = None

    def get_matrix(self, lines:list) -> None:
        # assumes lines are all the same length
        llen0 = len(lines[0])
        for line in lines:
            if len(line) != llen0:
                print(line)
                raise ValueError
        self.matrix = [list(line) for line in lines]

    def sliding_window_sum(self, r:int, c:int, cur_int=None, adj_symbol=False) -> int:
        new_int = None
        cur_adj_symbol = False
        if c == len(self.matrix[0]) or r == len(self.matrix):
            # reached the end
            return new_int if new_int is not None else (cur_int if cur_int is not None else 0)

        top, cur, bot = (
            self.matrix[r-1][c] if r-1 > 0 else None,
            self.matrix[r][c],
            self.matrix[r+1][c] if r+1 < len(self.matrix) else None
        )
        if isdigit(cur):
            new_int = (cur_int*10)+int(cur) if cur_int is not None else int(cur)
        else:
            new_int = None
        if any([c in SYMBOLS for c in [x if x is not None else NONSYM for x in [top, cur, bot]]]):
            cur_adj_symbol = True

        cnext = 0 if c == len(self.matrix[0])-1 else c+1
        rnext = r+1 if cnext == 0 else r
        if new_int is not None:
            # still on a number
            return self.sliding_window_sum(
                rnext,
                cnext,
                cur_int=new_int,
                adj_symbol=(cur_adj_symbol or adj_symbol)
            )

        elif cur_int is not None and new_int is None:
            # end of number, add it if adjacent to symbol and set cur_int to None
            return (cur_int if cur_adj_symbol or adj_symbol else 0) + \
                self.sliding_window_sum(
                    rnext,
                    cnext,
                    cur_int=new_int,
                    adj_symbol=cur_adj_symbol
                )

        elif new_int is None:
            # not on a number
            return self.sliding_window_sum(
                rnext,
                cnext,
                cur_int=new_int,
                adj_symbol=cur_adj_symbol
            )

    def run(self, lines:list):
        self.get_matrix(lines)
        ans = self.sliding_window_sum(r=0, c=0, cur_int=None, adj_symbol=False)
        self.log.info(f"ans: {ans}")
        return ans

class P2(P1):

    def sliding_window_assign(self, r:int, c:int, cur_int=None, adj_asterisks=[]) -> list:
        new_int = None
        cur_adj_asterisks = []
        if c == len(self.matrix[0]) or r == len(self.matrix):
            # reached the end
            return [{
                "val":new_int,
                "asterisks":adj_asterisks
            }] if new_int is not None else (
                [{
                    "val":cur_int,
                    "asterisks":adj_asterisks
                }] if cur_int is not None else []
            )

        top, cur, bot = (
            (r-1,c,self.matrix[r-1][c]) if r-1 > 0 else (r-1,c,None),
            (r,c,self.matrix[r][c]),
            (r+1,c,self.matrix[r+1][c]) if r+1 < len(self.matrix) else (r-1,c,None)
        )

        if isdigit(cur[2]):
            new_int = (cur_int*10)+int(cur[2]) if cur_int is not None else int(cur[2])
        else:
            new_int = None
        for tup in [top, cur, bot]:
            if tup[2] == '*':
                cur_adj_asterisks.insert(0,(tup[0],tup[1]))

        cnext = 0 if c == len(self.matrix[0])-1 else c+1
        rnext = r+1 if cnext == 0 else r
        if new_int is not None:
            # still on a number
            return self.sliding_window_assign(
                rnext,
                cnext,
                cur_int=new_int,
                adj_asterisks=(cur_adj_asterisks + adj_asterisks)
            )

        elif cur_int is not None and new_int is None:
            # end of number, add to dict if there are asterisks
            val = [{
                "val":cur_int,
                "asterisks":cur_adj_asterisks if cur_adj_asterisks != [] else adj_asterisks
            }] if cur_adj_asterisks != [] or adj_asterisks != [] else []
            return val + self.sliding_window_assign(
                    rnext,
                    cnext,
                    cur_int=new_int,
                    adj_asterisks=cur_adj_asterisks
                )

        elif new_int is None:
            # not on a number
            return self.sliding_window_assign(
                rnext,
                cnext,
                cur_int=new_int,
                adj_asterisks=cur_adj_asterisks
            )

    def get_gear_ratios(self, potential_gears:list) -> int:
        asterisks = [
            (pos, pair[1]) for pair in \
            map(lambda x: (x['asterisks'],x['val']),potential_gears) \
            for pos in pair[0]
        ]
        asterisks.sort()
        ratio_sum = 0
        for i in range(len(asterisks)-1):
            # exactly two values make a gear, not three or more
            stopval = asterisks[i+2] if i < len(asterisks)-2 else (None,None)
            if asterisks[i][0] == asterisks[i+1][0] and asterisks[i][0] != stopval[0]:
                ratio_sum += asterisks[i][1] * asterisks[i+1][1]
        return ratio_sum

    def run(self, lines:list):
        self.get_matrix(lines)
        potential_gears = self.sliding_window_assign(r=0, c=0, cur_int=None, adj_asterisks=[])
        ans = self.get_gear_ratios(potential_gears)
        self.log.info(f"ans: {ans}")
        return ans


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1],"r") as f:
        lines = [l.strip() for l in f.readlines()]
    P1().run(lines)
    P2().run(lines)