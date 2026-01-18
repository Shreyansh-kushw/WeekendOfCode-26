from tkinter import ttk

from tkinter import *
# from tkinter.ttk import *

class GUI:

    def __init__(self):
        
        self.root = Tk()
        self.root.title("Vanishing Tic-Tac-Toe")
        self.root.geometry("400x483")
        self.root.resizable(False, False)

        self.square_frame = Frame(self.root, width=100, height=100)
        self.square_frame.grid(column=0, row=0)

        # Creating a button inside this frame
        btn00 = Button(self.square_frame, text ="", bg = "white")
        btn00.config(height = 10, width = 18)
        btn00.grid(column = 0, row = 0)

        btn01 = Button(self.square_frame, text ="", bg = "white")
        btn01.config(height = 10, width = 18)
        btn01.grid(column = 15, row = 0)

        btn02 = Button(self.square_frame, text ="", bg = "white")
        btn02.config(height = 10, width = 18)
        btn02.grid(column = 30, row = 0)

        btn10 = Button(self.square_frame, text ="", bg = "white")
        btn10.config(height = 10, width = 18)
        btn10.grid(column = 0, row = 10)

        btn11 = Button(self.square_frame, text ="", bg = "white")
        btn11.config(height = 10, width = 18)
        btn11.grid(column = 15, row = 10)

        btn12 = Button(self.square_frame, text ="", bg = "white")
        btn12.config(height = 10, width = 18)
        btn12.grid(column = 30, row = 10)
        btn20 = Button(self.square_frame, text ="", bg = "white")
        btn20.config(height = 10, width = 18)
        btn20.grid(column = 0, row = 20)

        btn21 = Button(self.square_frame, text ="", bg = "white")
        btn21.config(height = 10, width = 18)
        btn21.grid(column = 15, row = 20)

        btn22 = Button(self.square_frame, text ="", bg = "white")
        btn22.config(height = 10, width = 18)
        btn22.grid(column = 30, row = 20)
        self.root.mainloop()

tester = GUI()