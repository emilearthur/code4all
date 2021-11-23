# Game status categories
# Change the values as you see fit
STATUS_WIN = "win"
STATUS_LOSE = "lose"
STATUS_ONGOING = "ongoing"


class Hangman:
    def __init__(self, word):
        self.remaining_guesses = 9
        self.status = STATUS_ONGOING
        self.word = word
        self.chars = set()

    def guess(self, char):
        if self.status != STATUS_ONGOING:
            raise ValueError("GameOver !")

        if (char in self.word) and (char not in self.chars):
            self.chars.add(char)
            if self.chars == set(self.word):
                self.status = STATUS_WIN
        else:
            if self.remaining_guesses == 0:
                self.status = STATUS_LOSE
            else:
                self.remaining_guesses -= 1

    def get_masked_word(self):
        return "".join(["_" if char not in self.chars else char for char
                        in self.word])

    def get_status(self):
        return self.status
