#!/usr/bin/env python3
import sys
import logging

colors = ["red","green","blue"]

class P1:
    def __init__(self):
        self.log = logging.getLogger(":".join([__file__,type(self).__name__]))

    def parse_game(self, line:str) -> dict:
        gamestr, roundstr = line.split(":")
        _, gamenum = gamestr.split(" ")
        roundlist = roundstr.split(";")
        rounds = []
        for rnd in roundlist:
            curr_round = {}
            colors = rnd.split(",")
            for color in colors:
                num, col = color.strip().split(" ")
                curr_round[col] = int(num)
            rounds.insert(0,curr_round)
        return {"game":int(gamenum),"rounds":rounds}


    def ispossible(self, game:dict, maximum:dict) -> bool:
        for rnd in game['rounds']:
            for k in colors:
                if k in rnd.keys() and rnd[k] > maximum[k]:
                    return False
        return True

    def run(self, lines:list) -> int:
        games = [self.parse_game(line) for line in lines]
        maximum = {"red":12, "green":13, "blue":14}
        ans = sum(
            [
                game['game'] if self.ispossible(game,maximum) else 0 for game in games
            ]
        )
        self.log.info(f"ans: {ans}")
        return ans

class P2(P1):
    def get_power(self, game:dict) -> int:
        least = {"red":float('-inf'), "green":float('-inf'), "blue":float('-inf')}
        for rnd in game['rounds']:
            for k in colors:
                if k in rnd.keys() and rnd[k] > least[k]:
                    least[k] = rnd[k]
        return least['red']*least['green']*least['blue']

    def run(self, lines:list) -> int:
        games = [self.parse_game(line) for line in lines]
        ans = sum([self.get_power(game) for game in games])
        self.log.info(f"ans: {ans}")
        return ans

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1],"r") as f:
        lines = [l.strip() for l in f.readlines()]
    P1().run(lines)
    P2().run(lines)