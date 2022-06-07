from ex12_utils import get_neighbors
BUTTON_FONT = ("Courier", 20)

class MyButton:
    def __init__(self, idx, letter, neighbors, tk_root):
        self.idx = idx
        self.letter = letter
        self.neighbors = neighbors
        self.tk_root = tk_root
        self.pressed = False
    def get_tk(self):
        tk.Button(self._root, text=self.letter, font=BUTTON_FONT)
