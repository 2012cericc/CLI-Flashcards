################################################################
#   Statistics class
################################################################
class Statistics:
    def __init__(self, num_cards):
        self.start_time = 0.0
        self.best_time = 0.0
        self.prev_time = 0.0
        self.time_taken = 0.0

        self.curr_card_num = 1
        self.num_cards = num_cards
        self.num_hidden = 0