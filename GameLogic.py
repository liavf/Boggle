from ex12_utils import *
from boggle_board_randomizer import *

WORDS_PATH = "boggle_dict.txt"
START_TIME = 180 #seconds

class GameLogic:
    """
    Game logic for boggle
    """
    def __init__(self):
        """
        Initiates game logic with words and start time for game
        """
        self.words = set(get_words(WORDS_PATH))
        self.start_time = START_TIME

    def calc_score(self, path_length: int) -> int:
        """
        Calculates score for path in game
        :param path_length: length of path for word
        """
        return path_length ** 2

    def find_in_words(self, word: str) -> bool:
        """
        Checks if a word is valid - not gueesed and in words list
        :param word: word to check
        :return:
        """
        return (word in self.words) and (word not in self.guesses)

    def check_called(self, word: str, path_length: int) -> bool:
        """
        Checks if a guessed word is valid and updates logic accordingly
        :param word: word to check
        :param path_length: length of word path
        :return: True if valid (and updated), else False
        """
        if self.find_in_words(word):
            self.guesses.add(word)
            self.score += self.calc_score(path_length)
            return True
        else:
            return False

    def new_round(self):
        """
        Initiates new game round
        """
        self.score = 0
        self.board = randomize_board()
        self.guesses = set()
        self.max_score_paths = max_score_paths(self.board, self.words)
