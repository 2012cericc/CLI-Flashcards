import sys
import random
import timeit
from flashcard import Flashcard

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
            #split each line from file into "lines" list
            lines = fo.read().splitlines()
        except FileNotFoundError:
            print("Error: {} not found".format(argv[i]))
            sys.exit(1)
        else:
            fo.close()
    
        #check file for formatting errors
        if check_file(lines, argv[i]) == False:
            for line in lines:
                temp = line.split(" ; ")
                card_objects.append(Flashcard(temp[0], temp[1]))
        else:
            found_error = True

    #exit if any error found in a flashcards file
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
#   print number of cards this round
################################################################
def print_num_cards(num_cards, num_hidden):
    print("Number of cards this round: %d" % (num_cards-num_hidden))
    print("")

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
    print("")

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
    print("")

################################################################
#   play through cards
################################################################
def play_cards(cards, stats):
    for i in range(len(cards)):
        if cards[i].hide is False:
            print("question:")
            cards[i].print_question()

            while True:
                prompt = input("> ")
                #quit
                if prompt == 'q':
                    print("Exiting flashcard program")
                    sys.exit()
                #next card
                elif prompt == 'n' or prompt == '':
                    print("answer:")
                    cards[i].print_answer()
                    break
                #hide card
                elif prompt == 'd':
                    cards[i].hide = True
                    stats.num_hidden += 1
                    break
                #print valid commands
                elif prompt == 'h':
                    print_options()
                else:
                    print("Invalid input")
            print('-' * 70)
    print("")

################################################################
#   display correct end round menu
################################################################
def end_round_prompt(stats, cards):
    print("End of round options:")

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
    print(" all cards are hidden, reset to play again")
    print(" (1) - reset cards and replay")
    #print(" (2) - add file")
    #print(" (3) - save file")
    print(" (4) - quit")

    while True:
        option = input("> ")
        if option == '1':
            reset_cards(cards)
            stats.num_hidden = 0
            break
        elif option == '4' or option == 'q':
            print("Exiting flashcard program")
            sys.exit()
        else:
            print("Invalid input")

################################################################
#   no cards hidden menu
################################################################
def none_hidden_menu(stats, cards):
    print(" (1) - replay")
    #print(" (2) - add file")
    #print(" (3) - save file")
    print(" (4) - quit")

    while True:
        option = input("> ")
        if option == '1':
            break
        elif option == '4' or option == 'q':
            print("Exiting flashcard program")
            sys.exit()
        else:
            print("Invalid input")

################################################################
#   some cards hidden menu
################################################################
def some_hidden_menu(stats, cards):
    print(" (1) - replay")
    print(" (2) - reset cards and replay")
    #print(" (3) - add file")
    #print(" (4) - save file")
    print(" (5) - quit")

    while True:
        option = input("> ")
        if option == '1':
            break
        elif option == '2':
            reset_cards(cards)
            stats.num_hidden = 0
            break
        elif option == '4' or option == 'q':
            print("Exiting flashcard program")
            sys.exit()
        else:
            print("Invalid input")