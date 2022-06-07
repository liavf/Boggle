from ex12_utils import get_neighbors
import tkinter as tk
BUTTON_FONT = ("Calibri", 15)
BUTTON_BG = "snow"

class MyButton:
    def __init__(self, idx, letter, neighbors, tk_root, command):
        self.idx = idx
        self.letter = letter
        self.neighbors = neighbors
        self.tk_root = tk_root
        self.pressed = False
        self.command = command(self)
        self.tk = tk.Button(self.tk_root, text=self.letter,
                            font=BUTTON_FONT, command=self.command,
                            width=1, height=1, bg=BUTTON_BG)
    def get_tk(self):
        b = tk.Button(self.tk_root, text=self.letter, font=BUTTON_FONT, command=self.command)
        # b.grid(idx[0], idx[1])
        return b

#
# my = MyButton(1, "l", [], tk.Tk(), lambda x: x)
# my.tk.configure(bg="red")
