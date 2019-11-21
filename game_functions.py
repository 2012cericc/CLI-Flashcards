import os
import sys
import glob
import random
import timeit
import re
from flashcard import Flashcard

################################################################
#   check number of arguments
################################################################
def check_arguments(argv):
    #incorrect number of arguments
    if len(argv) == 1:
        print("Usage: flashcards.py [text file]")
        sys.exit(1)

################################################################
#   check txt file for formatting errors
################################################################
def check_file(lines, arg):
    found_error = False
    if not lines:
        print("Error: \"%s\" is empty" % arg)
        found_error = True

    for i in range(len(lines)):
        if lines[i].find(" ; ") == -1:
            print("Error: formatting error in \"%s\" at line %d" % (arg, i+1))
            found_error = True
    return found_error

################################################################
#   open arg cards file add cards to cards list
################################################################
def open_file(arg, card_objects, stats):
    found_error = False
    #flashcards file not found
    try:
        fo = open(arg, "r")
        #split each line from file into "lines" list
        lines = fo.read().splitlines()
    except FileNotFoundError:
        print("Error: \"%s\" not found" % arg)
        found_error = True
    else:
        fo.close()
        #check file for formatting errors
        if check_file(lines, arg) == False:
            for line in lines:
                temp = line.split(" ; ")
                card_objects.append(Flashcard(temp[0], temp[1]))
                stats.num_cards += 1
        else:
            found_error = True

    return found_error

################################################################
#   given a directory, return usable .card files
################################################################
def find_files(dir, stats):
    choices = []
    card_files = glob.glob(dir + '/*.cards')

    for file_path in card_files:
        filename = os.path.split(file_path)[1]
        #do not allow previously imported files
        if filename not in stats.imported_files:
            choices.append(file_path)
    return choices

################################################################
#   print and let user select which .cards files to import
################################################################
def input_choices(files):
    unique_choices = []

    #print out potential files to add
    print("Enter indexes of files to import separated by spaces")
    for index in range(0, len(files)):
        filename = os.path.split(files[index])[1]
        print("  (%d) %s" % (index+1, filename))

    choices_input = input("> ")

    #blank input
    if choices_input == '':
        return unique_choices

    #guard invalid choices and repeat choices
    for choice in choices_input.split():
        if choice.isdigit() == False or int(choice)<=0 or int(choice)>len(files):
            print("Error: %s is not a valid choice" % choice)
        elif choice in unique_choices:
            print("Error: %s already imported" % files[int(choice)-1])
        else:
            unique_choices.append(choice)

    return unique_choices

################################################################
#   find all .cards files, let user choose which to import
################################################################
def choose_files(card_objects, stats, dir='.'):
    #check if given dir is a directory
    if not os.path.isdir(dir):
        print("Error: %s is not a directory" % dir)
        return False

    #find all .cards files in dir that have not been imported
    files = find_files(dir, stats)
    if not files:
        print("Error: no files to import from %s" % dir)
        return False

    choices = input_choices(files)
    if not choices:
        print("no files were imported")
        return False

    for choice in choices:
        filepath = files[int(choice)-1]
        if not open_file(filepath, card_objects, stats):
            filename = os.path.split(filepath)[1]
            stats.imported_files.append(filename)
            print("  added cards from %s" % filename)

    return True


################################################################
#   open cards from args
################################################################
def open_args(argv, card_objects, stats):
    found_error = False

    #loop to add cards in each argument
    for i in range(1, len(argv)):
        if open_file(argv[i], card_objects, stats):
            found_error = True

    return found_error

################################################################
#   add another flashcard file
################################################################
def add_file(cards, stats):
    """
    while True:
        print("Enter name of file to add:")
        print(" leave input blank to not add a file")
        filename = input("> ")
        print()

        if filename == '':
            break
        elif not open_file(filename, cards, stats):
            print("added: \"%s\" to the next round" % filename)
            print()
            break
    """
    while True:
        print("Enter directory path to look for card files")
        print(" leave input blank to use \"%s\"" % stats.original_directory)
        dir = input("> ")
        print()

        if dir == '':
            dir = stats.original_directory

        if not choose_files(cards, stats, dir):
            print()
            break


################################################################
#   save current set of flashcards
################################################################
def save_file(cards):
    new_filename = ''

    print("Enter name of file to be created:")
    print(" leave input blank to not create a new file")

    while True:
        new_filename = input("> ").rstrip()
        if new_filename == '':
            print()
            break
        #only allow certain characters in filename
        elif re.match("^[A-Za-z0-9-_.() ]*$", new_filename):
            try:
                fs = open(new_filename, "x")
            except FileExistsError:
                print("Error: filename \"%s\" already exists" % new_filename)
                print()
            else:
                for card in cards:
                    if card.hide == False:
                        print(card.question + " ; " + card.answer, file=fs)
                fs.close()
                print()
            break
        else:
            print("Invalid input")
            print(" only letters, numbers, and -_.() allowed")

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
#   print number of cards this round
################################################################
def print_num_cards(num_cards, num_hidden):
    print("Number of cards this round: %d" % (num_cards-num_hidden))
    print()

################################################################
#   convert seconds to (mins, secs) tuple
################################################################
def convert_seconds(seconds):
    m, s = divmod(seconds, 60)
    return (m, s)

################################################################
#   print best time
################################################################
def print_best_time(time_taken, best_time):
    new_best_time = 0.0

    if best_time == 0.0:
        new_best_time = time_taken
    else:
        new_best_time = min(time_taken, best_time)

    converted_time = convert_seconds(new_best_time)
    print("Best time:     %02d:%02d" % (converted_time[0], converted_time[1]))

    return new_best_time

################################################################
#   print prev time
################################################################
def print_prev_time(prev_time):
    if prev_time > 0:
        converted_time = convert_seconds(prev_time)
        print("Previous time: %02d:%02d" % (converted_time[0], converted_time[1]))

################################################################
#   print time taken
################################################################
def print_time_taken(time_taken):
    converted_time = convert_seconds(time_taken)
    print("Time taken:    %02d:%02d" % (converted_time[0], converted_time[1]))
    print()

################################################################
#   print all time stats
################################################################
def print_time_stats(stats):
    stats.time_taken = timeit.default_timer() - stats.start_time
    stats.best_time = print_best_time(stats.time_taken, stats.best_time)
    print_prev_time(stats.prev_time)
    print_time_taken(stats.time_taken)
    stats.prev_time = stats.time_taken

################################################################
#   print options
################################################################
def print_options():
    print("Valid commands:")
    print(" (h)elp - show this message")
    print(" (n)ext or () - print answer")
    print(" (d)elete - delete card from list")
    print(" (q)uit - quit the game")
    print()

################################################################
#   play through cards
################################################################
def play_cards(cards, stats):
    stats.curr_card_num = 1
    cards_in_round = stats.num_cards-stats.num_hidden

    for i in range(len(cards)):
        if cards[i].hide is False:
            print("question %d/%d:" % (stats.curr_card_num, cards_in_round))
            cards[i].print_question()

            while True:
                prompt = input("> ").rstrip()
                #quit
                if prompt == 'q':
                    print("Exiting flashcard program")
                    sys.exit()
                #next card
                elif prompt == 'n' or prompt == '':
                    stats.curr_card_num += 1
                    print("answer:")
                    cards[i].print_answer()
                    break
                #hide card
                elif prompt == 'd':
                    stats.curr_card_num += 1
                    cards[i].hide = True
                    stats.num_hidden += 1
                    break
                #print valid commands
                elif prompt == 'h':
                    print_options()
                else:
                    print("Invalid input")
            print('-' * 70)
    print()

################################################################
#   display correct end round menu
################################################################
def end_round_prompt(stats, cards):
    #show all cards hidden menu
    if stats.num_hidden == stats.num_cards:
        all_hidden_menu(stats, cards)
    #show no cards hidden menu
    elif stats.num_hidden == 0:
        none_hidden_menu(stats, cards)
    #show some cards hidden menu
    else:
        some_hidden_menu(stats, cards)

################################################################
#   all cards hidden menu
################################################################
def all_hidden_menu(stats, cards):
    print("End of round options:")
    print(" all cards are hidden, reset to play again")
    print(" (1) - reset cards and replay")
    print(" (2) - add file")
    print(" (3) - quit")

    option = input("> ").rstrip()
    if option == '1':
        reset_cards(cards)
        stats.num_hidden = 0
        return
    elif option == '2':
        add_file(cards, stats)
    elif option == '3' or option == 'q':
        print("Exiting flashcard program")
        sys.exit()
    else:
        print("Invalid input")
        print()

    end_round_prompt(stats, cards)

################################################################
#   no cards hidden menu
################################################################
def none_hidden_menu(stats, cards):
    print("End of round options:")
    print(" (1) - replay")
    print(" (2) - add file")
    print(" (3) - quit")

    option = input("> ").rstrip()
    if option == '1':
        return
    elif option == '2':
        add_file(cards, stats)
    elif option == '3' or option == 'q':
        print("Exiting flashcard program")
        sys.exit()
    else:
        print("Invalid input")
        print()

    end_round_prompt(stats, cards)

################################################################
#   some cards hidden menu
################################################################
def some_hidden_menu(stats, cards):
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
        reset_cards(cards)
        stats.num_hidden = 0
        return
    elif option == '3':
        add_file(cards, stats)
    elif option == '4':
        save_file(cards)
    elif option == '5' or option == 'q':
        print("Exiting flashcard program")
        sys.exit()
    else:
        print("Invalid input")
        print()

    end_round_prompt(stats, cards)
