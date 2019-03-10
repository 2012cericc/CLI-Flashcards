import textwrap

################################################################
#   Flashcard class
################################################################
class Flashcard:
    def __init__(self, question, answer, hide = False):
        self.question = question
        self.answer = answer
        self.hide = hide

    def print_card(self):
        """print all attributes of a flashcard for testing purposes"""
        print("%s, %s, %s" % (self.question, self.answer, self.hide))

    def print_question(self):
        question_lines = textwrap.wrap(self.question, width=68)
        for line in question_lines:
            print("  " + line)

    def print_answer(self):
        answer_lines = textwrap.wrap(self.answer, width=68)
        for line in answer_lines:
            print("  " + line)
