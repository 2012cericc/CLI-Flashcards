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
    
        #check file for errors
        if check_file(lines, argv[i]) == False:
            for line in lines:
                temp = line.split(" ; ")
                card_objects.append(Flashcard(temp[0], temp[1]))
        else:
            found_error = True

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
def play_cards(cards, num_hidden):
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
                    num_hidden += 1
                    break
                #print valid commands
                elif prompt == 'h':
                    print_options()
                else:
                    print("Invalid input")
            print('----------------------------------------')
    print("")
    return num_hidden

################################################################
#   ask to replay game
################################################################
def prompt_replay():
    while True:
        replay = input("Play again? (y/n):  ")
        if replay == 'n' or replay == 'q':
            print("Exiting, all cards complete")
            sys.exit()
        elif replay == 'y':
            break
        else:
            print("Invalid input")

################################################################
#   ask to reset hidden cards
################################################################
def prompt_reset(num_hidden, num_cards):
    if num_hidden > 0:
        while True:
            reset = input("Reset cards? (y/n): ")
            if reset == 'n':
                #check if all cards are hidden
                if num_hidden == num_cards:
                    print("All cards have been hidden, reset required")
                else:
                    return False
                    break
            elif reset == 'y':
                return True
                break
            elif reset == 'q':
                print("Exiting flashcard program")
                sys.exit()
            else:
                print("Invalid input")