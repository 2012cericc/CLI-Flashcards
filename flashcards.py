#!/usr/bin/env python3

"""
Basic flashcards program

Takes a file containing flashcards as an argument
Format of flashcards file: question ; answer
    Question and answer separated by " ; "
    Each card separated by a newline

Features
    Randomized card order each round
    Delete card from the list (does not delete from file)
        prevents card from being shown in next round
    resetting hidden status of all cards

Potential features to add
    detect incorrectly formatted flashcard files, print line number
    Input multiple flashcard files
    undo previous hide card
        only applies if previous command was delete
    create a GUI
        Tkinker?
    flag cards in file to never show them again
        or save non-hidden cards in a new flashcard file
    print time taken to complete a round
        based on honesty
"""
import sys
import os
import random

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
    
        #split file into Flashcard objects
        lines = fo.read().splitlines()
        fo.close()

        #if error found, do not append cards to list
        if check_file(lines, argv[i]) or found_error == True:
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

    cards = open_file(sys.argv) #open file and create list of card objects

    #game loop
    while replay != 'n':

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
                    reset_cards(cards)
                    break
                elif reset == 'q':
                    print("Exiting flashcard program")
                    sys.exit()
                else:
                    print("Invalid input")

        shuffle_cards(cards)
        os.system("clear") #clear terminal between rounds
        print_options()

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
                    elif prompt == 'n':
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
                print('')

        #replay?
        while True:
            replay = input("Play again? (y/n): ")
            if replay == 'n' or replay == 'q':
                print("Exiting, all cards completed")
                sys.exit()
            elif replay == 'y':
                break
            else:
                print("Invalid input")

    sys.exit()