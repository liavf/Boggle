
from ex12_utils import *
from boggle_board_randomizer import *
from time import strftime
WORDS_PATH = "boggle_dict.txt"
START_TIME = 180 #seconds

class GameLogic:
    def __init__(self):
        self.board = randomize_board()
        self.words = set(get_words(WORDS_PATH))
        self.score = 0
        self.start_time = START_TIME
        self.guesses = set() #words

    def new_round(self):
        self.board = randomize_board()

    def calc_score(self, word):
        return calculate_score(word)

    def update_score(self, word):
        self.score += self.calc_score(word)

    def find_in_words(self, word):
        return word in self.words

    def check_called(self, word):
        if self.find_in_words(word):
            if word
            if self.current_guess.upper() in self.game_logic.words:
                if self.current_guess not in self.game_logic.guesses:
                    self.game_logic.guesses.add(self.current_guess)
                    self._all_guess_frame.configure(
                        text="\n".join(self.game_logic.guesses))
                    self._score += len(self.current_guess)
                    self._score_label.configure(text=self._score)
            self.current_guess = ""
            self._current_guess_label.configure(text=self.current_guess)
            self.reset_board()

    def main_loop(self):
        # while play:
        pass