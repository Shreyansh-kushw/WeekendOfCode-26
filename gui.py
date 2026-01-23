from tkinter import *


class GUI:
    """Class that handles the GUI"""

    def __init__(self) -> None:

        self.root = Tk()
        self.root.title("Vanishing Tic-Tac-Toe")
        self.root.geometry("428x550")
        self.root.resizable(False, False)

        self.square_frame = Frame(self.root, width=100, height=100)
        self.square_frame.grid(column=0, row=0)

        # Creating a button inside this frame
        self.btn00 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn00.config(height=2, width=4)
        self.btn00.grid(column=0, row=0)

        self.btn01 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn01.config(height=2, width=4)
        self.btn01.grid(column=15, row=0)

        self.btn02 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn02.config(height=2, width=4)
        self.btn02.grid(column=30, row=0)

        self.btn10 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn10.config(height=2, width=4)
        self.btn10.grid(column=0, row=10)

        self.btn11 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn11.config(height=2, width=4)
        self.btn11.grid(column=15, row=10)

        self.btn12 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn12.config(height=2, width=4)
        self.btn12.grid(column=30, row=10)

        self.btn20 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn20.config(height=2, width=4)
        self.btn20.grid(column=0, row=20)

        self.btn21 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn21.config(height=2, width=4)
        self.btn21.grid(column=15, row=20)

        self.btn22 = Button(self.square_frame, text="", bg="white", font=("Arial", 36))
        self.btn22.config(height=2, width=4)
        self.btn22.grid(column=30, row=20)
