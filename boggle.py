from ex12_utils import *
from boggle_board_randomizer import *
import tkinter as tk
from time import strftime
WORDS_PATH = "boggle_dict.txt"
IN_GUESS = 'red'
TURN_TIME = 60*3 #SECONDS

class Game:
    def __init__(self):
        self.board = randomize_board()
        self.words = get_relevant_words(WORDS_PATH, self.board)
        self.score = 0
        self.guesses = set() #words


    def run_round(self, guess):
        word = is_valid_path(self.board, guess, self.words)
        if word:
            guess.add(words)

    def main_loop(self):
        # while play:
        pass


class GameDisplay:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.current_guess = ""
        self._root = tk.Tk()
        #title
        self._root.title('@ grade us 105 @')
        self._title = tk.Label(self._root, text = "Boggle", font = ("Curier",
                                                                  30))
        self._title.pack()
        #play_game
        self._play_button = tk.Button(self._root, text="Play", command = \
                                self._play_round, font = ("Courier", 30))
        self._play_button.pack(side=tk.BOTTOM)
        #timer
        self._timer = TURN_TIME
        self._time_label = tk.Label(self._root, font = ("Courier", 20),
                                    text=f"time: {self._timer // 60} mins"
                                    f" {self._timer % 60} secs")
        self._time_label.pack(side=tk.TOP)
        #score
        self._score = 0
        self._score_label = tk.Label(self._root, font = ("Courier", 20),
                                     text = f"score: {self._score}")
        self._score_label.pack()
        #currect selection label
        self._display_label = tk.Label(self._root, font = ("Courier", 30))
        self._display_label.pack(side=tk.TOP)
        frame = tk.Frame(self._root)
        frame.pack()
        self.buttons = [tk.Button(frame) for _ in range(len(
            self.game_logic.board)** 2)]
        self._fill_board(frame)

    def _fill_board(self, frame):
        board = self.game_logic.board
        indexes = get_all_indexes(len(board))
        button_num = 0
        for index in indexes:
            x, y = index
            letter = board[x][y]
            #todo: change color
            self.buttons[button_num].configure(text = letter, command =
            self._button_event(letter, button_num), font = ("Courier", 30),
                                               bg = "yellow")
            #button[= tk.Button(frame, text = letter, command =
            #self._button_event(letter, button_num), font = ("Courier", 30))
            #print(button)
            self.buttons[button_num].grid(row = x, column = y)
            button_num += 1

    def _button_event(self, letter, button_num):
        def button_event_helper():
            self.current_guess += letter
            self._display_label.configure(text = self.current_guess)
            self.buttons[button_num].configure(text = "-", bg = IN_GUESS)
        return button_event_helper

    def _play_round(self):
        self._timer = TURN_TIME
        self.countdown()
        return

    def start(self):
        self._root.mainloop()

    def countdown(self):
        if self._timer == 0:
            self._time_label.configure(text="times up")
        else:
            self._time_label.configure(text=f"time: {self._timer//60} mins"
                                            f" {self._timer%60} secs")
            self._timer -= 1
            self._root.after(1000, self.countdown) #every_second

    # def _check_end(self):
    # def _mouse_press(self):
    # def _get_location_clicked(self):??
    #
    # def change_color(self, x, y, color):
    # def show_score(self):
    # def end_round(self):

if __name__ == '__main__':
    game_logic = Game()
    gd = GameDisplay(game_logic)
    gd.start()
