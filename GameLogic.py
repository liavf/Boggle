
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
        self.max_score = 5

    def new_round(self):
        self.board = randomize_board()

    def calc_score(self, word):
        return calculate_score(word)

    def update_score(self, word):
        self.score += self.calc_score(word)

    def find_in_words(self, word):
        return (word in self.words) and (word not in self.guesses)

    def check_called(self, word):
        if self.find_in_words(word):
            self.guesses.add(word)
            self.update_score(word)
            return True
        else:
            return False

    def get_max_score(self):
        return max_score_paths_2(self.board, self.words)


    def main_loop(self):
        # while play:
        pass