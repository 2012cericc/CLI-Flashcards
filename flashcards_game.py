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
    gf.check_arguments(sys.argv)  #check number of arguments

    stats = Statistics()
    cards = []

    while True:
        if gf.choose_files(cards, stats, sys.argv[1]):
            stats.original_directory = sys.argv[1]
            break
        print()
    
    
    #game loop
    while True:
        gf.shuffle_cards(cards)
        gf.print_options()
        gf.print_num_cards(stats.num_cards, stats.num_hidden)
        
        #stats.start_time = timeit.default_timer()
        stats.start_timer()
        gf.play_cards(cards, stats)
        
        #gf.print_time_stats(stats)
        stats.print_time_stats()
        
        gf.end_round_prompt(stats, cards)

        os.system("clear")  #clear terminal between rounds
    sys.exit()

