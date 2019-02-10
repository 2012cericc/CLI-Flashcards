#!/usr/bin/env python3

import sys
import os
import random
import timeit

################################################################
#   Flashcard class
################################################################
class Flashcard:
    def __init__(self, question, answer, hide = False):
        self.question = question
        self.answer = answer
        self.hide = hide

    def print_card(self):
        print("%s, %s, %s" % (self.question, self.answer, self.hide))

################################################################
#   check txt file for formatting errors
################################################################
def check_file(lines, arg):
    found_error = False

    for i in range(len(lines)):
        if lines[i].find(" ; ") == -1:
            print("Error: formatting error in \"%s\" at line %d" % (arg, i+1))
            found_error = True

    return found_error

################################################################
#   open txt file and return card objects
################################################################
def open_file(argv):
    card_objects = [] #list to hold all card objects
    found_error = False

    #incorrect number of arguments
    if len(argv) == 1:
        print("Usage: flashcards.py [text file]")
        sys.exit(1)

    #loop to add cards in each argument
    for i in range(1, len(argv)):

        #flashcards file not found
        try:
            fo = open(argv[i], "r")
        except FileNotFoundError:
            print("Error: {} not found".format(argv[i]))
            sys.exit(1)
    
        #split each line from file into "lines" list
        lines = fo.read().splitlines()
        fo.close()

        #if error found, do not append cards to card_objects
        if found_error == True or check_file(lines, argv[i]):
            found_error = True
        else:
            for line in lines:
                temp = line.split(" ; ")
                card_objects.append(Flashcard(temp[0], temp[1]))

    #exit if error found in a flashcards file
    if found_error == True:
        sys.exit(1)

    return card_objects

################################################################
#   shuffle flashcards
################################################################
def shuffle_cards(cards):
    for i in range(0, len(cards)):
        rand_idx = random.randint(0, len(cards)-1)
        cards[i], cards[rand_idx] = cards[rand_idx], cards[i]

################################################################
#   reset hidden cards
################################################################
def reset_cards(cards):
    for card in cards:
        card.hide = False

################################################################
#   print time taken
################################################################
def convert_seconds(seconds):
    m, s = divmod(seconds, 60)
    return (m, s)

################################################################
#   print options
################################################################
def print_options():
    print("Valid commands:")
    print(" (h)elp - show this message")
    print(" (n)ext - print answer and next prompt")
    print(" (d)elete - delete card from list")
    print(" (q)uit - quit the game")
    print('')

################################################################
#   main
################################################################
if __name__ == '__main__':
    hidden_cards = 0 #track number of cards hidden
    replay = '' #play again input
    prev_time = (0, 0)

    cards = open_file(sys.argv) #open file and create list of card objects

    #game loop
    while replay != 'n':
        os.system("clear") #clear terminal between rounds

        start_time = timeit.default_timer()
        shuffle_cards(cards)
        print_options()
        
        print("Previous time: %02d:%02d" % (prev_time[0], prev_time[1]))
        print('')

        #play through the cards
        for i in range(len(cards)):
            if cards[i].hide is False:
                print("question: %s" % cards[i].question)

                while True:
                    prompt = input("> ")
                    #quit
                    if prompt == 'q':
                        print("Exiting flashcard program")
                        sys.exit()
                    #next card
                    elif prompt == 'n' or prompt == '':
                        print("answer: %s" % cards[i].answer)
                        break
                    #hide card
                    elif prompt == 'd':
                        cards[i].hide = True
                        hidden_cards += 1
                        break
                    #print valid commands
                    elif prompt == 'h':
                        print_options()
                    else:
                        print("Invalid input")
                print('----------------------------------------')

        #print time taken to complete the round
        time_taken = timeit.default_timer() - start_time
        converted_time = convert_seconds(time_taken)
        prev_time = converted_time
        print("Time taken: %02d:%02d" % (time_taken[0], time_taken[1]))
        print('')

        #replay?
        while True:
            replay = input("Play again? (y/n): ")
            if replay == 'n' or replay == 'q':
                print("Exiting, all cards complete")
                sys.exit()
            elif replay == 'y':
                break
            else:
                print("Invalid input")

        #reset hidden cards?
        if hidden_cards > 0 and replay == 'y':
            while True:
                reset = input("Reset all cards? (y/n): ")
                if reset == 'n':
                    #check if all cards are hidden
                    if hidden_cards == len(cards):
                        print("All cards have been hidden, reset cards")
                    else:
                        break
                elif reset == 'y':
                    hidden_cards = 0
                    reset_cards(cards) #unhide all cards
                    break
                elif reset == 'q':
                    print("Exiting flashcard program")
                    sys.exit()
                else:
                    print("Invalid input")
    sys.exit()