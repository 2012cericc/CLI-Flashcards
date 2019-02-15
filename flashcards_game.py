#!/usr/bin/env python3

import sys
import os
import timeit
import game_functions as gf

################################################################
#   main
################################################################
if __name__ == '__main__':
    hidden_cards = 0 #track number of cards hidden
    replay = '' #play again input
    prev_time = 0.0
    best_time = 0.0

    cards = gf.open_file(sys.argv) #open file and create list of card objects

    #game loop
    while True:
        os.system("clear") #clear terminal between rounds

        start_time = timeit.default_timer()

        gf.shuffle_cards(cards)
        gf.print_options()

        hidden_cards += gf.play_cards(cards, hidden_cards)

        time_taken = timeit.default_timer() - start_time
        best_time = gf.print_best_time(time_taken, best_time)
        gf.print_prev_time(prev_time)
        gf.print_time_taken(time_taken)
        prev_time = time_taken

        gf.prompt_replay()

        if gf.prompt_reset(hidden_cards, len(cards)):
            hidden_cards = 0
            gf.reset_cards(cards)
  
    sys.exit()