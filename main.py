import tkinter as tk
from random import randint

list_of_words: list[str]


def random_word() -> str:
    return list_of_words[randint(0, len(list_of_words) - 1)]


class Game:
    def __init__(self, gui: tk.Tk):

        self.gameOverState: bool = False
        self.wonState: bool = False
        self.mistakes: int = 0
        self.word: str = ''
        self.final_word: str = ''

        self.gui: tk.Tk = gui
        self.gui.title("HangMan")
        self.gui.geometry("400x400")
        self.gui.resizable(False, False)

        self.wordField: tk.Label = tk.Label(master=self.gui, font=('Arial', 15))
        self.wordField.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

        self.set_init_values()
        self.canvas = tk.Canvas(master=self.gui, height=200, width=200)
        self.canvas.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.stateMessage = tk.Label(master=self.gui, font=('Arial', 22))
        self.stateMessage.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

        self.frame = tk.Frame(master=self.gui)
        self.frame.place(relx=0.05, rely=0.7)
        row_ = 0
        for ch in range(0, 26):
            txt = chr(ch + ord('a'))
            btn = tk.Button(master=self.frame, text=txt.upper(), width=4,
                            borderwidth=0.5, command=lambda char=txt: self.check_and_do(char))
            col = ch % 10
            if col == 0:
                row_ += 1
            btn.grid(column=col, row=row_)
        self.resetButton = tk.Button(master=self.frame, width=4, text='Reset', borderwidth=0.5, command=self.reset)
        self.row_ = row_

        self.draw_init()
        self.gui.mainloop()

    def set_init_values(self):
        self.word = random_word()
        self.mistakes = 0
        self.wonState = False
        self.gameOverState = False

        self.final_word = '*' * len(self.word)
        self.update_word_field()

    def check_and_do(self, char):
        if char:
            if self.wonState:
                self.draw_state("YOU WON")
            elif self.gameOverState:
                self.draw_state("YOU LOST")
            elif char in self.word:
                if '*' in self.final_word:
                    self.write_letter(char)
                    if '*' not in self.final_word:
                        self.wonState = True
                        self.draw_state("YOU WON")
            elif self.mistakes <= 5:
                self.mistakes += 1
                self.draw_body_parts(self.mistakes)
                if self.mistakes == 6:
                    self.gameOverState = True
                    self.draw_state("YOU LOST")

    def update_word_field(self):
        self.wordField.config(text=self.final_word)

    def write_letter(self, char):
        word = []
        for i in range(len(self.word)):
            if self.word[i] == char:
                word.append(char.upper())
            else:
                word.append(self.final_word[i])
        self.final_word = ''.join(word)
        self.update_word_field()

    def reset(self):
        if self.gameOverState or self.wonState:
            self.set_init_values()
            self.canvas.delete(tk.ALL)
            self.draw_init()
            self.resetButton.pack_forget()
            self.stateMessage.config(text='')
            self.resetButton.grid_forget()

    def draw_state(self, message):
        self.resetButton.grid(column=6, row=self.row_)
        if self.gameOverState:
            self.final_word = self.word.upper()
            self.update_word_field()
            self.stateMessage.config(fg='red')
        else:
            self.stateMessage.config(fg='green')
        self.stateMessage.config(text=message)

    def draw_init(self):
        self.canvas.create_line(20, 190, 90, 190, width=3)  # bottom line
        self.canvas.create_line(55, 190, 55, 20, width=3)  # middle line
        self.canvas.create_line(54, 20, 140, 20, width=3)  # top line
        self.canvas.create_line(140, 19, 140, 40, width=3)  # bottom-top line

    def draw_body_parts(self, index):
        if index == 1:
            self.canvas.create_oval((120, 40), (160, 80), width=3)  # draw head
        elif index == 2:
            self.canvas.create_line(140, 80, 140, 150, width=3)  # draw body
        elif index == 3:
            self.canvas.create_line(140, 90, 160, 130, width=3)  # draw right hand
        elif index == 4:
            self.canvas.create_line(140, 90, 120, 130, width=3)  # draw left hand
        elif index == 5:
            self.canvas.create_line(140, 149, 160, 185, width=3)  # draw right leg
        elif index == 6:
            self.canvas.create_line(140, 149, 120, 185, width=3)  # draw left leg


if __name__ == '__main__':
    with open('words', 'r') as f:
        list_of_words = [x[0:-1].strip().lower() for x in f.readlines()]
    root = tk.Tk()
    Game(root)
