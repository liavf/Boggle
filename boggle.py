from ex12_utils import *
from boggle_board_randomizer import *
WORDS_PATH = "boogle_dict.txt"

class Game:
    def __init__(self):
        self.board = randomize_board()
        self.words = get_relevant_words(WORDS_PATH, self.board)
        self.score = score
        self.guessed_paths = {}

    def run_round(self, guess):
        #assuming guess is a valid path
        word = get_word_from_path(self.board, guess)
        if word in self.words:
            guess
    def main_loop(self, guess):

class GameDisplay:
    pass