from typing import Tuple, List, Callable, Any
import tkinter as tk

Location = Tuple[int, int]
# BUTTON_FONT = ("Calibri", 20)
BUTTON_BG = "snow"

class MyButton:
    """
    Button object for boggle game
    """
    def __init__(self, idx: Location, letter: str, neighbors: List[Location],
                 tk_root: Any, command: Callable):
        """
        Initiates button object
        :param idx: location tuple in board
        :param letter: letter/s of button
        :param neighbors: list of neighbor locations
        :param tk_root: tk root that the button is a part of
        :param command: command linked to button
        """
        self.idx = idx
        self.letter = letter
        self.neighbors = neighbors
        self.tk_root = tk_root
        self.pressed = False
        self.command = command(self)
        self.tk = tk.Button(self.tk_root, text=self.letter,
                            command=self.command)
    # def get_tk(self):
    #     return tk.Button(self.tk_root, text=self.letter, font=BUTTON_FONT,
    #                command=self.command)
