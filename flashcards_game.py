#!/usr/bin/env python3

import sys
import os
import timeit
import game_functions as gf
from statistics import Statistics

################################################################
#   main
################################################################
if __name__ == '__main__':
    cards = gf.open_file(sys.argv) #open file and create list of card objects
    stats = Statistics(len(cards))

    #game loop
    while True:
        os.system("clear") #clear terminal between rounds

        gf.shuffle_cards(cards)
        gf.print_options()
        gf.print_num_cards(stats.num_cards, stats.num_hidden)

        stats.start_time = timeit.default_timer()
        gf.play_cards(cards, stats)
        gf.print_time_stats(stats)

        gf.end_round_prompt(stats, cards)
    sys.exit()