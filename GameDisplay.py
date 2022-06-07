from GameLogic import GameLogic
from MyButton import MyButton
from ex12_utils import get_all_indexes, get_neighbors
import tkinter as tk

from time import strftime
IN_GUESS = "lavender blush"
BACKGROUND = "mint cream"
SCORE_FONT = ("Calibri", 20)
DEFAULT_FONT = ("Calibri", 20)
BUTTONS_FONT = ("Calibri", 35)
PLAY_FONT = ("Calibri", 35)
DEFAULT_BG = "snow"

COLORS = {"DARK": {"DEFAULT_BG": "grey"}, "LIGHT": {"DEFAULT_BG": "mint "
                                                                  "cream"}}




class GameDisplay:
    def __init__(self):
        self.current_guess = ""
        self._root = tk.Tk()
        self._root.geometry("450x450")
        self.mode = "LIGHT"
        self._root.configure(bg=COLORS[self.mode]["DEFAULT_BG"])
        self.win = False
        self.start_menu()

    def start_menu(self):
        self.gl = GameLogic()
        # title
        self.photo_boggle = tk.PhotoImage(file=r"title_image.png")
        self.title_label = tk.Label(self._root, image=self.photo_boggle, 
                                    bg=COLORS[self.mode]["DEFAULT_BG"])
        self.title_label.pack(side=tk.TOP)
        self._root.title("Boggle")
        # play_game
        self._mode_button = tk.Checkbutton(self._root, text='dark mode',
                                        bg=COLORS[self.mode]["DEFAULT_BG"], command= self._change_color)
        self._mode_button.pack(side=tk.BOTTOM)
        self._play_button = tk.Button(self._root, text="Play", command= \
        self._play_round, font=PLAY_FONT)
        self._play_button.pack(side=tk.BOTTOM)

    def _change_color(self):
        if self.mode == "LIGHT":
            self.mode = "DARK"
        else:
            self.mode ="LIGHT"
        #repaint
        self._root.configure(bg=COLORS[self.mode]["DEFAULT_BG"])
        self.title_label.configure(bg=COLORS[self.mode]["DEFAULT_BG"])
        self._mode_button.configure(bg=COLORS[self.mode]["DEFAULT_BG"])



    def _play_round(self):
        self.game_gui()
        self._timer = self.gl.start_time
        self.countdown()
        self._init_board()
        # if hasattr(self, "title_label"):
        #     self.title_label.destroy()
        if hasattr(self, "_play_button"):
            self._play_button.destroy()
        if hasattr(self, "_play_again"):
            self._play_again.destroy()
        if hasattr(self, "win_label"):
            self.win_label.destroy()

    def game_gui(self):
        # title
        self.title_label.destroy()
        self.photo_boggle = tk.PhotoImage(file=r"small_boggle.png")
        self.title_label = tk.Label(self._root, image=self.photo_boggle, bg=COLORS[self.mode]["DEFAULT_BG"])
        self.title_label.pack(side=tk.TOP)
        # timer
        self._timer = self.gl.start_time
        self._time_label = tk.Label(self._root, bg=COLORS[self.mode]["DEFAULT_BG"],
                                    font=DEFAULT_FONT,
                                    text=f"time: {self._timer // 60} mins"
                                         f" {self._timer % 60} secs")
        self._time_label.pack(side=tk.TOP)
        # score
        self._score_label = tk.Label(self._root, font= SCORE_FONT,
                                     text=f"score: {self.gl.score}", bg=COLORS[self.mode]["DEFAULT_BG"])
        self._score_label.pack()

        # check answer
        self._check_answer_label = tk.Button(self._root, font=PLAY_FONT,
                                             command=self.check_answer,
                                             text="check")
        self._check_answer_label.pack(side=tk.BOTTOM)

        # all guesses
        self._all_guess_frame = tk.Frame(self._root, bg=COLORS[self.mode]["DEFAULT_BG"])
        self._all_guess_frame.place(x=50, y=170)
        # current selection label
        self._current_guess_label = tk.Label(self._all_guess_frame,
                                             font=DEFAULT_FONT, bg=COLORS[self.mode]["DEFAULT_BG"])
        self._current_guess_label.pack(side=tk.TOP)
        self._all_guess_title = tk.Label(self._all_guess_frame, bg=COLORS[self.mode]["DEFAULT_BG"],
                                         text="all guesses", font=DEFAULT_FONT)
        self._all_guess_title.pack(side=tk.TOP)
        self._all_guess = tk.Label(self._all_guess_frame, bg=COLORS[self.mode]["DEFAULT_BG"],
                                   text="\n".join(self.gl.guesses),
                                   font=DEFAULT_FONT)
        self._all_guess.pack()


    def _init_board(self):
        self._buttons = []
        # frame
        self._button_frame = tk.Frame(self._root, bg=COLORS[self.mode]["DEFAULT_BG"])
        self._button_frame.place(x=250, y=200)
        # create buttons
        indexes = get_all_indexes(len(self.gl.board))
        for idx in indexes:
            x, y = idx
            letter = self.gl.board[x][y]
            neighbors = get_neighbors(idx, len(self.gl.board))
            button = MyButton(idx, letter, neighbors, self._button_frame,
                              self._button_event)
            button.tk.configure(font=BUTTONS_FONT)
            button.tk.grid(row=x, column=y, padx=1, pady=1)
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
           self._all_guess.configure(text="\n".join(self.gl.guesses))
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
            self.win_label = tk.Label(self._root, text="you won",
                                      font=DEFAULT_FONT, bg=COLORS[self.mode]["DEFAULT_BG"])
            self.win_label.pack()
        self.win = False
        self._play_again = tk.Button(self._root, text="Play Again", command=
        self._play_round, font=DEFAULT_FONT)
        self._play_again.pack(side=tk.BOTTOM)


if __name__ == '__main__':
    gd = GameDisplay()
    gd.start()