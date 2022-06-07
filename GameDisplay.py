from GameLogic import GameLogic
from MyButton import MyButton
from ex12_utils import get_all_indexes, get_neighbors
import tkinter as tk
from time import strftime
IN_GUESS = 'red'

class GameDisplay:
    def __init__(self):
        self.current_guess = ""
        self._root = tk.Tk()
        self.start_menu()
        self.win = False
        # # start menu
        # #title
        # self.photo_boggle = tk.PhotoImage(file=r"title_image.png")
        # self.title_button = tk.Button(self._root, image=self.photo_boggle)
        # self.title_button.pack(side=tk.TOP)
        # self._root.title("Boggle")
        # #play_game
        # self._play_button = tk.Button(self._root, text="Play", command = \
        #                         self._play_round, font = ("Courier", 30))
        # self._play_button.pack(side=tk.BOTTOM)
        # #timer
        # self._timer = self.gl.start_time
        # self._time_label = tk.Label(self._root, font = ("Courier", 20),
        #                             text=f"time: {self._timer // 60} mins"
        #                             f" {self._timer % 60} secs")
        # self._time_label.pack(side=tk.TOP)
        # #score
        # self._score_label = tk.Label(self._root, font = ("Courier", 20),
        #                              text = f"score: {self.gl.score}")
        # self._score_label.pack()
        # #current selection label
        # self._current_guess_label = tk.Label(self._root, font = ("Courier", 30))
        # self._current_guess_label.pack(side=tk.TOP)
        #
        # # check answer
        # self._check_answer_label = tk.Button(self._root, font=("Courier", 30), command=self.check_answer, text="check")
        # self._check_answer_label.pack(side=tk.BOTTOM)
        #
        # # all guesses
        # self._all_guess_frame = tk.Label(self._root, bg="blue")
        # self._all_guess_frame.pack()

    def start_menu(self):
        self.gl = GameLogic()
        # title
        self.photo_boggle = tk.PhotoImage(file=r"title_image.png")
        self.title_button = tk.Button(self._root, image=self.photo_boggle)
        self.title_button.pack(side=tk.TOP)
        self._root.title("Boggle")
        # play_game
        self._play_button = tk.Button(self._root, text="Play", command= \
        self._play_round, font=("Courier", 30))
        self._play_button.pack(side=tk.BOTTOM)

    def _play_round(self):
        self.game_gui()
        self._timer = self.gl.start_time
        self.countdown()
        self._init_board()
        if hasattr(self, "title_button"):
            self.title_button.destroy()
        if hasattr(self, "_play_button"):
            self._play_button.destroy()
        if hasattr(self, "_play_again"):
            self._play_again.destroy()
        if hasattr(self, "win_label"):
            self.win_label.destroy()

    def game_gui(self):
        # timer
        self._timer = self.gl.start_time
        self._time_label = tk.Label(self._root, font=("Courier", 20),
                                    text=f"time: {self._timer // 60} mins"
                                         f" {self._timer % 60} secs")
        self._time_label.pack(side=tk.TOP)
        # score
        self._score_label = tk.Label(self._root, font=("Courier", 20),
                                     text=f"score: {self.gl.score}")
        self._score_label.pack()
        # current selection label
        self._current_guess_label = tk.Label(self._root, font=("Courier", 30))
        self._current_guess_label.pack(side=tk.TOP)

        # check answer
        self._check_answer_label = tk.Button(self._root, font=("Courier", 30),
                                             command=self.check_answer,
                                             text="check")
        self._check_answer_label.pack(side=tk.BOTTOM)

        # all guesses

        self._all_guess_frame_title = tk.Label(self._root, bg="old lace", text="all guesses")
        self._all_guess_frame_title.pack(side = tk.LEFT)
        self._all_guess_frame = tk.Label(self._root, bg="old lace", text="\n".join(self.gl.guesses))
        self._all_guess_frame.pack(side = tk.LEFT)


    def _init_board(self):
        self._buttons = []
        # frame
        self._button_frame = tk.Frame(self._root)
        self._button_frame.pack()
        # create buttons
        indexes = get_all_indexes(len(self.gl.board))
        for idx in indexes:
            x, y = idx
            letter = self.gl.board[x][y]
            neighbors = get_neighbors(idx, len(self.gl.board))
            button = MyButton(idx, letter, neighbors, self._button_frame, self._button_event)
            button.tk.grid(row=x, column=y)
            self._buttons.append(button)

    def _button_event(self, button):
        def _button_event_helper():
            self.current_guess += button.letter
            self._current_guess_label.configure(text=self.current_guess)
            button.pressed = True
            button.tk.configure(background=IN_GUESS, state="disabled")
            for but in self._buttons:
                if but.idx in button.neighbors and not but.pressed:
                    but.tk.configure(state="normal")
                else:
                    but.tk.configure(state="disabled")
        return _button_event_helper

    def start(self):
        self._root.mainloop()

    def countdown(self):
        if self._timer == 0 or self.win:
            self._time_label.configure(text="time's up")
            self.play_again()
        else:
            self._time_label.configure(text=f"time: {self._timer//60} mins"
                                            f" {self._timer%60} secs")
            self._timer -= 1
            self._root.after(1000, self.countdown) #every_second

    def check_answer(self):
        if self.gl.check_called(self.current_guess):
           self._all_guess_frame.configure(text="\n".join(self.gl.guesses))
           self._score_label.configure(text=f"score: {self.gl.score}")
           if self.gl.max_score <= self.gl.score:
               self.win = True
        self.current_guess = ""
        self._current_guess_label.configure(text=self.current_guess)
        self.reset_board()

    def reset_board(self):
        for button in self._buttons:
            button.tk.configure(state="normal", bg="white")
            button.pressed = False

    def play_again(self):
        self._time_label.destroy()
        self._button_frame.destroy()
        self._score_label.destroy()
        self._current_guess_label.destroy()
        self._check_answer_label.destroy()
        self._all_guess_frame.destroy()
        if self.win:
            self.win_label = tk.Label(self._root, text="you won")
            self.win_label.pack()
        self.win = False
        self._play_again = tk.Button(self._root, text="Play Again", command= self._play_round, font=("Courier", 30))
        self._play_again.pack(side=tk.BOTTOM)


if __name__ == '__main__':
    gd = GameDisplay()
    gd.start()