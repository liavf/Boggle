from GameLogic import GameLogic
from MyButton import MyButton
from ex12_utils import get_all_indexes, get_neighbors
import tkinter as tk
from gui_consts import *

class GameDisplay:
    """
    Gui class for boggle game
    """
    def __init__(self):
        """
        Initiates game display with necessary variables and calls start menu
        """
        self.current_guess = ""
        self.current_guess_path = 0
        self._root = tk.Tk()
        self._root.geometry(WINDOW_SIZE)
        self.mode = LIGHT
        self._root.configure(bg=COLORS[self.mode][DEFAULT_BG])
        self.gl = GameLogic()
        self._root.title(WINDOW_TITLE)
        self._start_menu()
        self.timer_started = False

    def start(self):
        """
        Starts game loop
        """
        self._root.mainloop()

    def _start_menu(self):
        """
        Start menu for boggle game
        """
        # title image
        self._photo_boggle = tk.PhotoImage(file=BIG_TITLE)
        self._title_label = tk.Label(self._root, image=self._photo_boggle,
                                    bg=COLORS[self.mode][DEFAULT_BG])
        self._title_label.pack(side=tk.TOP)
        # change color mode
        self._mode_button = tk.Checkbutton(self._root, text=MODE_BUTTON,
                                        bg=COLORS[self.mode][DEFAULT_BG], command= self._change_color)
        self._mode_button.pack(side=tk.BOTTOM)
        # play_game
        self._play_button = tk.Button(self._root, text=PLAY_BUTTON, command= \
                                        self._play_round, font=PLAY_FONT)
        self._play_button.pack(side=tk.BOTTOM)

    def _change_color(self):
        """
        Change color variable command for mode button
        """
        if self.mode == LIGHT:
            self.mode = DARK
        else:
            self.mode = LIGHT
        #repaint
        self._root.configure(bg=COLORS[self.mode][DEFAULT_BG])
        self._title_label.configure(bg=COLORS[self.mode][DEFAULT_BG])
        self._mode_button.configure(bg=COLORS[self.mode][DEFAULT_BG])

    def _play_round(self):
        """
        Runs one round of boggle game
        """
        self._clean_window()
        #change attributes and run gui for round
        self.gl.new_round()
        self._init_board()
        self.current_guess = ""
        self.current_guess_path = 0
        self._round_gui() #creates gui
        self._countdown()

    def _round_gui(self):
        """
        Runs game gui for round
        :return:
        """
        # change main title to smaller one
        self._title_label.destroy()
        self._photo_boggle = tk.PhotoImage(file=SMALL_TITLE)
        self._title_label = tk.Label(self._root, image=self._photo_boggle,
                                     bg=COLORS[self.mode][DEFAULT_BG])
        self._title_label.pack(side=tk.TOP)

        # creates timer
        self._timer = self.gl.start_time
        self._time_label = tk.Label(self._root, bg=COLORS[self.mode][DEFAULT_BG],
                                    font=DEFAULT_FONT,
                                    text=TIME_LABEL_STR.format(self._timer//60, self._timer%60))
        self._time_label.pack(side=tk.TOP)
        # score label
        self._score_label = tk.Label(self._root, font= SCORE_FONT,
                                     text=SCORE_TITLE + f"{self.gl.score}",
                                    bg=COLORS[self.mode][DEFAULT_BG])
        self._score_label.pack()

        # check answer label
        self._check_answer_label = tk.Button(self._root, font=DEFAULT_FONT,
                                             command=self._check_answer,
                                             text=CHECK_BUTTON)
        self._check_answer_label.place(x=CHECK_X, y=CHECK_Y)

        # restart label
        self._restart_label = tk.Button(self._root, font=DEFAULT_FONT,
                                    command=self._restart, text=RESTART_BUTTON)
        self._restart_label.place(x=RESTART_X, y=RESTART_Y)
        #### all guesses frame ###
        self._all_guess_frame = tk.Frame(self._root, bg=COLORS[self.mode][DEFAULT_BG])
        self._all_guess_frame.place(x=GUESS_FRAME_X, y=GUESS_FRAME_Y)
        # current selection label
        self._current_guess_label = tk.Label(self._all_guess_frame,
                                             font=DEFAULT_FONT, bg=COLORS[self.mode][DEFAULT_BG])
        self._current_guess_label.pack(side=tk.TOP)
        # all guesses title
        self._all_guess_title = tk.Label(self._all_guess_frame, bg=COLORS[self.mode][DEFAULT_BG],
                                         text=ALL_GUESSES_TITLE,
                                         font=DEFAULT_FONT)
        self._all_guess_title.pack(side=tk.TOP)
        # all guesses frame
        self._all_guess = tk.Label(self._all_guess_frame, bg=COLORS[self.mode][DEFAULT_BG],
                                   text="\n".join(self.gl.guesses),
                                   font=GUESSES_FONT)
        self._all_guess.pack()

    def _init_board(self):
        """
        Initiates board with buttons
        """
        ### buttons frame
        self._buttons = []
        self._button_frame = tk.Frame(self._root, bg=COLORS[self.mode][DEFAULT_BG])
        self._button_frame.place(x=BOARD_FRAME_X, y=BOARD_FRAME_Y)
        # create buttons
        indexes = get_all_indexes(len(self.gl.board), len(self.gl.board[0]))
        for idx in indexes:
            x, y = idx
            letter = self.gl.board[x][y]
            neighbors = get_neighbors(idx, len(self.gl.board), len(self.gl.board[0]))
            button = MyButton(idx, letter, neighbors, self._button_frame,
                              self._button_event)
            button.tk.configure(font=BUTTONS_FONT,width=BUTTON_LENGTH,
                                height=BUTTON_LENGTH, bg="black")
            button.tk.grid(row=x, column=y, padx=PAD, pady=PAD)
            self._buttons.append(button)

    def _button_event(self, button):
        """
        handles button pressing by disabling all unvalid buttons
        :param button: button object that was pressed
        """
        def _button_event_helper():
            self.current_guess += button.letter
            self.current_guess_path += 1
            self._current_guess_label.configure(text=self.current_guess)
            button.pressed = True
            button.tk.configure(background=IN_GUESS, state="disabled")
            for but in self._buttons:
                if but.idx in button.neighbors and not but.pressed:
                    but.tk.configure(state="normal")
                else:
                    but.tk.configure(state="disabled")
        return _button_event_helper

    def _countdown(self):
        if not self.timer_started:
            self.timer_started = True
            self._root.after(1000, self.tick)

    def tick(self):
        if self._timer == 0:
            # if self._timer == 0 or self.win
            # self._time_label.configure(text=TIMES_UP_TEXT)
            self._play_again()
        else:
            self._time_label.configure(text=TIME_LABEL_STR.format(self._timer//60, self._timer%60))
            self._timer -= 1
        self._root.after(1000, self.tick)  # every_second

    def _check_answer(self):
        """
        Checks if answer is valid, updates score accordingly and resets
        buttons of borad
        """
        if self.gl.check_called(self.current_guess, self.current_guess_path):
           self._all_guess.configure(text="\n".join(self.gl.guesses))
           self._score_label.configure(text=SCORE_TITLE + f"{self.gl.score}")
           # if len(self.gl.max_score_paths) == len(self.gl.guesses):
           #     self.win = True
        self.current_guess = ""
        self.current_guess_path = 0
        self._current_guess_label.configure(text=self.current_guess)
        self._reset_board()

    def _reset_board(self):
        """
        Resets buttons after answer is checked
        """
        for button in self._buttons:
            button.tk.configure(state="normal", bg=BUTTON_BG)
            button.pressed = False

    def _restart(self):
        """
        Restarts board and round
        """
        self._clean_window()
        self._play_round()

    def _play_again(self):
        """
        Restarts board and asks user if they want to play again
        :return:
        """
        self._clean_window()
        # if self.win:
        #     self._win_label = tk.Label(self._root, text=WIN_TEXT,
        #                               font=DEFAULT_FONT, bg=COLORS[self.mode][DEFAULT_BG])
        #     self._win_label.pack()
        # # self.win = False
        self._game_finished_label = tk.Label(self._root, text=GAME_OVER_TEXT,
                             font=DEFAULT_FONT, bg=COLORS[self.mode][DEFAULT_BG])
        self._game_finished_label.place(x=GAME_OVER_X, y=GAME_OVER_Y)
        self._play_again_label = tk.Button(self._root, text=PLAY_AGAIN_TEXT,
                                      command=
                                        self._restart, font=DEFAULT_FONT)
        self._play_again_label.pack(side=tk.BOTTOM)

    def _clean_window(self):
        """
        Removes all widget from window
        """
        for widget in self._root.winfo_children():
            widget.destroy()