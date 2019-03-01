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

        stats.num_hidden = gf.play_cards(cards, stats.num_hidden)

        gf.print_time_stats(stats)

        gf.prompt_replay()

        if gf.prompt_reset(stats.num_hidden, len(cards)):
            num_hidden = 0
            gf.reset_cards(cards)
  
    sys.exit()