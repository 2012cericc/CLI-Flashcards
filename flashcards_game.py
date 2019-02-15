#!/usr/bin/env python3

import sys
import os
import timeit
import game_functions as gf

################################################################
#   main
################################################################
if __name__ == '__main__':
    num_hidden = 0 #track number of cards hidden
    prev_time = 0.0
    best_time = 0.0

    cards = gf.open_file(sys.argv) #open file and create list of card objects

    #game loop
    while True:
        os.system("clear") #clear terminal between rounds

        start_time = timeit.default_timer()

        gf.shuffle_cards(cards)
        gf.print_options()

        gf.print_num_cards(len(cards), num_hidden)

        num_hidden = gf.play_cards(cards, num_hidden)

        time_taken = timeit.default_timer() - start_time
        best_time = gf.print_best_time(time_taken, best_time)
        gf.print_prev_time(prev_time)
        gf.print_time_taken(time_taken)
        prev_time = time_taken

        gf.prompt_replay()

        if gf.prompt_reset(num_hidden, len(cards)):
            num_hidden = 0
            gf.reset_cards(cards)
  
    sys.exit()