#!/usr/bin/env python3
import sys
import logging
import re

class P1:
    def __init__(self):
        self.log = logging.getLogger(":".join([__file__,type(self).__name__]))

    def get_cards(self,lines:list) -> dict:
        cards = {}
        for cardline in lines:
            cardline_split = cardline.split(": ") # get everything after the card identifier
            card_id = re.findall(r'[0-9]+',cardline_split[0])[0]
            nums = cardline_split[1].split(" | ")
            winning_nums    = [int(x) for x in re.findall(r'[0-9]+',nums[0])]
            card_nums       = [int(x) for x in re.findall(r'[0-9]+',nums[1])]
            cards[card_id] = {
                "winners":winning_nums,
                "card_nums":card_nums
            }
        return cards

    def sum_card_values(self, cards:dict) -> int:
        total = 0
        for card in cards.values():
            #print(card)
            cardval = 0
            for num in card['card_nums']:
                if num in card['winners']:
                    #print(f"winning number {num}")
                    cardval = cardval*2 if cardval != 0 else 1
            #print(f"cardval: {cardval}")
            total += cardval
        return total


    def run(self, lines:list):
        cards = self.get_cards(lines)
        ans = self.sum_card_values(cards)
        self.log.info(f"ans: {ans}")
        return ans

class P2(P1):

    def get_cards(self,lines:list) -> dict:
        cards = {}
        for cardline in lines:
            cardline_split = cardline.split(": ") # get everything after the card identifier
            card_id = re.findall(r'[0-9]+',cardline_split[0])[0]
            nums = cardline_split[1].split(" | ")
            winning_nums    = [int(x) for x in re.findall(r'[0-9]+',nums[0])]
            card_nums       = [int(x) for x in re.findall(r'[0-9]+',nums[1])]
            cards[card_id] = {
                "winners":winning_nums,
                "card_nums":card_nums,
                "copies":1
            }
        return cards

    def sum_card_values(self, cards:dict) -> int:
        # we can make some shortcuts here, since it's just 
        # copies we can simply track how many times we need 
        # to replicate the effects of the first card value.
        cards = cards.copy()
        for card_id in range(1,len(cards)+1):
            card = cards[str(card_id)]
            cardval = 0
            for num in card['card_nums']:
                if num in card['winners']:
                    cardval += 1
            # the next <cardval> number of cards get a copy
            if cardval != 0:
                for i in range(card['copies']):
                    for j in range(1,cardval+1):
                        cards[str(card_id+j)]['copies'] += 1
        return sum([cards[k]['copies'] for k in cards])

    def run(self, lines:list):
        cards = self.get_cards(lines)
        ans = self.sum_card_values(cards)
        self.log.info(f"ans: {ans}")
        return ans

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1],"r") as f:
        lines = [l.strip() for l in f.readlines()]
    P1().run(lines)
    P2().run(lines)