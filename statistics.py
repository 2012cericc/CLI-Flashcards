import timeit

################################################################
#   Statistics class
################################################################
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
       
    ################################################################
    #   Timer related methods
    ################################################################
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

    
