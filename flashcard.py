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