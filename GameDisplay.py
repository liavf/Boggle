class GameDisplay:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.current_guess = ""
        self.all_guesses = []
        self._root = tk.Tk()
        #title
        photo_boggle = tk.PhotoImage(file=r"title_image.png")
        title_button = tk.Button(self._root, image=photo_boggle)
        title_button.pack(side=tk.RIGHT)
        self._root.title("Boggle")
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
        self._current_guess_label = tk.Label(self._root, font = ("Courier", 30))
        self._current_guess_label.pack(side=tk.TOP)

        # check answer
        self._check_answer_label = tk.Button(self._root, font=("Courier", 30), command=self.check_answer, text="check")
        self._check_answer_label.pack(side=tk.BOTTOM)

        # all guesses
        self._all_guess_frame = tk.Label(self._root, bg="blue")
        self._all_guess_frame.pack()

        #buttons
        self._button_frame = tk.Frame(self._root)
        self._button_frame.pack()
        self._buttons = [tk.Button(self._button_frame, font=("Courier", 20)) \
                         for _ in range(len(self.game_logic.board)** 2)]

    def _fill_board(self):
        board = self.game_logic.board
        indexes = get_all_indexes(len(board))
        button_num = 0
        for index in indexes:
            x, y = index
            letter = board[x][y]
            self._buttons[button_num].configure(text=letter, command=self._button_event(letter, button_num))
            self._buttons[button_num].grid(row = x, column = y)
            button_num += 1

    def _button_event(self, letter, button_num):
        def buttoner():
            self.current_guess += letter
            self._current_guess_label.configure(text = self.current_guess)
            self._buttons[button_num].configure(background = IN_GUESS, state="disabled")
        return buttoner

    def _play_round(self):
        self._timer = TURN_TIME
        self.countdown()
        self._fill_board()
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

    def check_answer(self):
        if self.current_guess.upper() in self.game_logic.words:
            if self.current_guess not in self.game_logic.guesses:
                self.game_logic.guesses.add(self.current_guess)
                self._all_guess_frame.configure(text="\n".join(self.game_logic.guesses))
                self._score += len(self.current_guess)
                self._score_label.configure(text=self._score)
        self.current_guess = ""
        self._current_guess_label.configure(text=self.current_guess)
        self.reset_board()

    def reset_board(self):
        for button in self._buttons:
            button.configure(state="normal", bg="white")

    # def _check_end(self):
    # def _mouse_press(self):
    # def _get_location_clicked(self):??
    #
    # def change_color(self, x, y, color):
    # def show_score(self):
    # def end_round(self):
