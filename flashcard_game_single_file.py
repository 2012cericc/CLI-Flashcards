#!/usr/bin/env python3

import os
import sys
import glob
import random
import timeit
import re
import textwrap

"""################################################################
    Flashcards_Game contains methods related to gameplay and
    .cards file management.
"""################################################################
class Flashcards_Game():
    def __init__(self, argv):
        self.check_arguments(argv)
        self.cards = []
        self.stats = Statistics()
    
        # ensure cards are imported before starting game
        while True:
            if self.import_files(argv[1]) and self.cards:
                self.stats.original_directory = sys.argv[1]
                break
            print()
        print()
        
        # game loop
        while True:
            self.shuffle_cards()
            
            self.print_interface()
            print()
            self.stats.print_num_cards()
            
            self.stats.start_timer()
            self.play_game()
            
            self.stats.print_time_stats()
            
            self.end_round_prompt()
            os.system("clear")  # clear terminal between rounds
        sys.exit()
        
    """################################################################
       Gameplay methods
    """################################################################
    def check_arguments(self, argv):
        # incorrect number of arguments
        if len(argv) != 2:
            print("Usage: flashcards.py [.cards]")
            sys.exit(1)
    
    # plays through the current deck of cards
    def play_game(self):
        self.stats.curr_card_num = 1
        cards_in_round = self.stats.num_cards - self.stats.num_hidden

        for i in range(len(self.cards)):
            if self.cards[i].hide is False:
                print("question %d/%d:" % (self.stats.curr_card_num, cards_in_round))
                self.cards[i].print_question()

                while True:
                    prompt = input("> ").rstrip()
                    # quit
                    if prompt == 'q':
                        print("Exiting flashcard program")
                        sys.exit()
                    # next card
                    elif prompt == 'n' or prompt == '':
                        self.stats.curr_card_num += 1
                        print("answer:")
                        self.cards[i].print_answer()
                        break
                    # hide card
                    elif prompt == 'd':
                        self.stats.curr_card_num += 1
                        self.cards[i].hide = True
                        self.stats.num_hidden += 1
                        break
                    # print valid commands
                    elif prompt == 'h':
                        self.print_interface()
                    else:
                        print("Invalid input")
                print('-' * 70)
        print()

    def shuffle_cards(self):
        for i in range(0, len(self.cards)):
            rand_idx = random.randint(0, len(self.cards)-1)
            self.cards[i], self.cards[rand_idx] = self.cards[rand_idx], self.cards[i]
        
    def reset_cards(self):
        for card in self.cards:
            card.hide = False
        
    def print_num_cards(self):
        num_not_hidden = self.stats.num_cards - self.stats.num_hidden
        print("Number of cards this round: %d" % num_not_hidden)
        
    def print_interface(self):
        print("Valid commands:")
        print(" (h)elp - show this message")
        print(" (n)ext or () - print answer")
        print(" (d)elete - delete card from list")
        print(" (q)uit - quit the game")
        
    def end_round_prompt(self):
        # show all cards hidden menu
        if self.stats.num_hidden == self.stats.num_cards:
            self.all_hidden_menu()
        # show no cards hidden menu
        elif self.stats.num_hidden == 0:
            self.none_hidden_menu()
        # show some cards hidden menu
        else:
           self.some_hidden_menu()
        
    def all_hidden_menu(self):
        print("End of round options:")
        print(" all cards are hidden, reset to play again")
        print(" (1) - reset cards and replay")
        print(" (2) - add file")
        print(" (3) - quit")

        option = input("> ").rstrip()
        if option == '1':
            self.reset_cards()
            self.stats.num_hidden = 0
            return
        elif option == '2':
            self.add_file()
        elif option == '3' or option == 'q':
            print("Exiting flashcard program")
            sys.exit()
        else:
            print("Invalid input")
            print()

        self.end_round_prompt()
        
    def none_hidden_menu(self):
        print("End of round options:")
        print(" (1) - replay")
        print(" (2) - add file")
        print(" (3) - quit")

        option = input("> ").rstrip()
        if option == '1':
            return
        elif option == '2':
            self.add_file()
        elif option == '3' or option == 'q':
            print("Exiting flashcard program")
            sys.exit()
        else:
            print("Invalid input")
            print()

        self.end_round_prompt()
        
    def some_hidden_menu(self):
        print("End of round options:")
        print(" (1) - replay")
        print(" (2) - reset cards and replay")
        print(" (3) - add file")
        print(" (4) - save file")
        print(" (5) - quit")

        option = input("> ").rstrip()
        if option == '1':
            return
        elif option == '2':
            self.reset_cards()
            self.stats.num_hidden = 0
            return
        elif option == '3':
            self.add_file()
        elif option == '4':
            self.save_cards()
        elif option == '5' or option == 'q':
            print("Exiting flashcard program")
            sys.exit()
        else:
            print("Invalid input")
            print()

        self.end_round_prompt()
    
    """################################################################
       File management methods
       
       Using a directory path, valid .cards files will be found and
       the player can choose which ones to import into the current
       flashcard deck. In the event of a .cards file formatting error,
       the file will not be imported and the error location will be
       reported.
    """################################################################
    def import_files(self, directory):
        # check if given dir is a directory
        if not os.path.isdir(directory):
            print("Error: \"%s\" is not a directory" % directory)
            return False
        # get list of .cards files in dir that have not been imported
        choices = self.find_files(directory)
        if not choices:
            print("Error: no files to import from \"%s\"" % directory)
            return False
        # let user choose which .cards files to import           
        chosen_files = self.select_files(choices)
        if not chosen_files:
            print("no files were imported")
            return False
        # import each file and check for errors
        for choice in chosen_files:
            filepath = choices[int(choice)-1]
            if self.open_file(filepath):
                filename = os.path.split(filepath)[1]
                self.stats.imported_files.append(filename)
                print("  added cards from \"%s\"" % filename)
        return True
    
    # find/return list of valid card files in directory
    def find_files(self, directory):        
        choices = []
        card_files = glob.glob(directory + '/*.cards')

        for file_path in card_files:
            filename = os.path.split(file_path)[1]
            # do not use previously imported files
            if filename not in self.stats.imported_files:
                choices.append(file_path)
        return choices
    
    # print and allow user to choose which files to import
    def select_files(self, choices):
        chosen_files = []
        # print out potential files to add with numbered index
        print("Enter indexes of files to import separated by spaces")
        for i in range(0, len(choices)):
            filename = os.path.split(choices[i])[1]
            print("  (%d) %s" % (i+1, filename))

        choices_input = input("> ")
        
        if choices_input == 'q':
            print("Exiting flashcard program")
            sys.exit()
        elif choices_input == '': # blank input
            return chosen_files

        # guard against invalid choices and repeated choices
        for choice in choices_input.split(' '):
            if choice.isdigit() == False or int(choice)<=0 or int(choice)>len(choices):
                print("Error: \"%s\" is not a valid choice" % choice)
            # do not import the same choice more than once
            elif choice in chosen_files:
                print("Error: \"%s\" already imported" % choices[int(choice)-1])
            else:
                chosen_files.append(choice)

        return chosen_files
    
    # open file, check for errors, create and append cards to cards list
    def open_file(self, path):
        try:
            fo = open(path, "r")
            # split each line from file into "lines" list
            lines = fo.read().splitlines()
        except FileNotFoundError:
            print("Error: \"%s\" not found" % path)
            return False
        else:
            fo.close()
            # check file for formatting errors
            if self.check_file(lines, path) == True:
                for line in lines:
                    temp = line.split(" ; ")
                    self.cards.append(Flashcard(temp[0], temp[1]))
                    self.stats.num_cards += 1
            else:
                return False
        return True
    
    # check each line from a file for errors and report them
    def check_file(self, lines, path):
        error = False
        if not lines:
            print("Error: \"%s\" is empty" % path)
            return False

        for i in range(len(lines)):
            if lines[i].find(" ; ") == -1:
                print("Error: formatting error in \"%s\" at line %d" % (path, i+1))
                error = True
        if error:
            return False
        else:
            return True

    # specify a directory from which to add new cards mid-game
    def add_file(self):
        print("Enter directory path to look for card files")
        print(" leave input blank to use \"%s\"" % self.stats.original_directory)
        directory = input("> ")
        print()

        if directory == '':
            directory = self.stats.original_directory

        self.import_files(directory)
        print()
    
    # allow user to save current set of cards to a new file
    def save_cards(self):
        #new_filename = ''
        print("Enter name of file to be created:")
        print(" leave input blank to not create a new file")

        while True:
            new_filename = input("> ").rstrip()
            if new_filename == '':
                print()
                break
            # only allow certain characters in filename
            elif re.match("^[A-Za-z0-9-_.() ]*$", new_filename):
                try:
                    fs = open(new_filename, "x")
                except FileExistsError:
                    print("Error: filename \"%s\" already exists" % new_filename)
                    print()
                else:
                    for card in self.cards:
                        if card.hide == False:
                            print(card.question + " ; " + card.answer, file=fs)
                    fs.close()
                    print()
                break
            else:
                print("Invalid input")
                print(" only letters, numbers, and -_.() allowed")
                
"""################################################################
   Flashcard class
"""################################################################
class Flashcard:
    def __init__(self, question, answer, hide = False):
        self.question = question
        self.answer = answer
        self.hide = hide

    def print_card(self):
        """print all attributes of a flashcard for testing purposes"""
        print("%s, %s, %s" % (self.question, self.answer, self.hide))

    def print_question(self):
        if self.hide:
            print("This card is hidden")
        question_lines = textwrap.wrap(self.question, width=68)
        for line in question_lines:
            print("  " + line)

    def print_answer(self):
        answer_lines = textwrap.wrap(self.answer, width=68)
        for line in answer_lines:
            print("  " + line)
            
"""################################################################
   Statistics class
"""################################################################
class Statistics:
    def __init__(self):
        self.start_time = 0.0
        self.best_time = 0.0
        self.prev_time = 0.0
        self.time_taken = 0.0

        self.curr_card_num = 1  # index of card being displayed
        self.num_cards = 0      # total number of cards in the stack
        self.num_hidden = 0     # number of cards currently hidden

        self.original_directory = ""
        self.imported_files = [] # list of card files that have been imported

    def print_imported_files(self):
        print("Currently imported files:")
        for filename in self.imported_files:
            print("    " + filename)
            
    def print_num_cards(self):
        print("Number of cards this round: %d" % (self.num_cards - self.num_hidden))
       
    """################################################################
       Timer related methods
    """################################################################
    def start_timer(self):
        self.start_time = timeit.default_timer()
        
    def print_time_stats(self):
        self.time_taken = timeit.default_timer() - self.start_time
        self.print_best_time()
        self.print_prev_time()
        self.print_time_taken()
        print()
        self.prev_time = self.time_taken
        
    def convert_seconds(self, seconds):
        m, s = divmod(seconds, 60)
        return (m, s)
    
    def print_best_time(self):
        if self.best_time == 0.0:
            self.best_time = self.time_taken
        else:
            self.best_time = min(self.time_taken, self.best_time)

        converted_time = self.convert_seconds(self.best_time)
        print("Best time:     %02d:%02d" % (converted_time[0], converted_time[1]))

    def print_prev_time(self):
        if self.prev_time > 0:
            converted_time = self.convert_seconds(self.prev_time)
            print("Previous time: %02d:%02d" % (converted_time[0], converted_time[1]))
            
    def print_time_taken(self):
        converted_time = self.convert_seconds(self.time_taken)
        print("Time taken:    %02d:%02d" % (converted_time[0], converted_time[1]))
        
"""################################################################
   main
"""################################################################
if __name__ == '__main__':
    game = Flashcards_Game(sys.argv)
