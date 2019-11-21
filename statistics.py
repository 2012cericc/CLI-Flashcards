################################################################
#   Statistics class
################################################################
class Statistics:
    def __init__(self):
        self.start_time = 0.0
        self.best_time = 0.0
        self.prev_time = 0.0
        self.time_taken = 0.0

        self.curr_card_num = 1 # index of card being displayed
        self.num_cards = 0 # total number of cards in the stack
        self.num_hidden = 0 # number of cards currently hidden

        self.original_directory = ""
        self.imported_files = [] # list of card files that have been imported

    def print_imported_files(self):
        print("Currently imported files:")
        for file in self.imported_files:
            print("    " + file)