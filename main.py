from collections import deque
from tkinter import *
from pyautogui import alert
import os
import threading

class GUI:

    def __init__(self):
        
        self.root = Tk()
        self.root.title("Vanishing Tic-Tac-Toe")
        self.root.geometry("461x647")
        self.root.resizable(False, False)

        self.square_frame = Frame(self.root, width=100, height=100)
        self.square_frame.grid(column=0, row=0)

        # Creating a button inside this frame
        self.btn00 = Button(self.square_frame, text ="", bg = "white")
        self.btn00.config(height = 10, width = 18)
        self.btn00.grid(column = 0, row = 0)

        self.btn01 = Button(self.square_frame, text ="", bg = "white")
        self.btn01.config(height = 10, width = 18)
        self.btn01.grid(column = 15, row = 0)

        self.btn02 = Button(self.square_frame, text ="", bg = "white")
        self.btn02.config(height = 10, width = 18)
        self.btn02.grid(column = 30, row = 0)

        self.btn10 = Button(self.square_frame, text ="", bg = "white")
        self.btn10.config(height = 10, width = 18)
        self.btn10.grid(column = 0, row = 10)

        self.btn11 = Button(self.square_frame, text ="", bg = "white")
        self.btn11.config(height = 10, width = 18)
        self.btn11.grid(column = 15, row = 10)

        self.btn12 = Button(self.square_frame, text ="", bg = "white")
        self.btn12.config(height = 10, width = 18)
        self.btn12.grid(column = 30, row = 10)

        self.btn20 = Button(self.square_frame, text ="", bg = "white")
        self.btn20.config(height = 10, width = 18)
        self.btn20.grid(column = 0, row = 20)

        self.btn21 = Button(self.square_frame, text ="", bg = "white")
        self.btn21.config(height = 10, width = 18)
        self.btn21.grid(column = 15, row = 20)

        self.btn22 = Button(self.square_frame, text ="", bg = "white")
        self.btn22.config(height = 10, width = 18)
        self.btn22.grid(column = 30, row = 20)
        

class GameState:

    def __init__(self):
        self.winning_scenerio = [
            [(0,0),(0,1),(0,2)],
            [(1,0),(1,1),(1,2)],
            [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)],
            [(0,1),(1,1),(2,1)],
            [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)],
            [(0,2),(1,1),(2,0)]
        ]

        self.board = {
            (0,0) : " ",
            (0,1) : " ",
            (0,2) : " ",
            (1,0) : " ",
            (1,1) : " ",
            (1,2) : " ",
            (2,0) : " ",
            (2,1) : " ",
            (2,2) : " ",
        }
        self.ui = GUI()

        self.button_position = {
            (0,0) : self.ui.btn00,
            (0,1) : self.ui.btn01,
            (0,2) : self.ui.btn02,
            (1,0) : self.ui.btn10,
            (1,1) : self.ui.btn11,
            (1,2) : self.ui.btn12,
            (2,0) : self.ui.btn20,
            (2,1) : self.ui.btn21,
            (2,2) : self.ui.btn22,
        }

        self.Player_X = "X"
        self.Player_O = "O"
        
        self.update_board()
        
        self.Player_X_queue = deque()
        self.Player_O_queue = deque()

        self.plays = 0
        self.current_player = "X" 

        self.scores = {
            "X" : -1,
            "O" : 1,
            "tie" : 0,
        }

    def update_board(self):
        # print("updating")
        self.ui.btn00.config(text=self.board[(0,0)], command= lambda: self.button_handler((0,0), self.button_position[(0,0)]))
        self.ui.btn01.config(text=self.board[(0,1)], command= lambda: self.button_handler((0,1), self.button_position[(0,1)]))
        self.ui.btn02.config(text=self.board[(0,2)], command= lambda: self.button_handler((0,2), self.button_position[(0,2)]))
        self.ui.btn10.config(text=self.board[(1,0)], command= lambda: self.button_handler((1,0), self.button_position[(1,0)]))
        self.ui.btn11.config(text=self.board[(1,1)], command= lambda: self.button_handler((1,1), self.button_position[(1,1)]))
        self.ui.btn12.config(text=self.board[(1,2)], command= lambda: self.button_handler((1,2), self.button_position[(1,2)]))
        self.ui.btn20.config(text=self.board[(2,0)], command= lambda: self.button_handler((2,0), self.button_position[(2,0)]))
        self.ui.btn21.config(text=self.board[(2,1)], command= lambda: self.button_handler((2,1), self.button_position[(2,1)]))
        self.ui.btn22.config(text=self.board[(2,2)], command= lambda: self.button_handler((2,2), self.button_position[(2,2)]))
    
    def button_handler(self, position:tuple[int], button):
        self.play(position)
        button.config(state = "disabled")
        self.update_board()
        print(3)
        self.game_state_check()

    def play(self, position:tuple[int]):

        if self.current_player == "X":
            self.Player_X_queue.append(position)
            # if len(self.Player_X_queue) < 3:
            #     self.Player_X_queue.append(position)

            # else:
            #     removed = self.Player_X_queue.popleft()
            #     self.board[removed] = " "
            #     self.button_position[removed].config(state="active")
            #     self.Player_X_queue.append(position)
            
            if self.board[position] == " ":
                self.board[position] = self.current_player
            else:
                pass
            
            self.current_player = "O"
            self.update_board()
            self.computer_turn()
            
        else:
            self.Player_O_queue.append(position)
            # if len(self.Player_O_queue) < 3:
            #     self.Player_O_queue.append(position)

            # else:
            #     removed = self.Player_O_queue.popleft()
            #     self.board[removed] = " "
            #     self.button_position[removed].config(state="active")
            #     self.Player_O_queue.append(position)
            
            if self.board[position] == " ":
                self.board[position] = self.current_player
            else:
                pass
            
            self.current_player = "X"
            self.update_board()

    def check_availability(self, keys:list[tuple[int]]):
        new_list = []
        for key in keys:
            if self.board[key] != " ":
                pass
            else:
                new_list.append(key)  
        
        return new_list

    def computer_turn(self):

        best_score = float("-inf")

        possibilites = list(map(self.check_availability, [list(self.board.keys())]))[0]
        if possibilites:
            for positions in possibilites:
                self.board[positions] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[positions] = " "
                if score > best_score:
                    best_score = score
                    best_move = positions
            self.button_handler(best_move, self.button_position[best_move])
        
        else:
            self.game_state_check()

    def minimax(self, board, depth:int = 1, isMaximizing:bool = True):
        
        winner = self.game_state_check(minimaxing=True)

        if winner is not None:
            return winner
        
        if isMaximizing:
            best_score = float("-inf")
            possibilites = list(map(self.check_availability, [list(self.board.keys())]))[0]
            for positions in possibilites:
                self.board[positions] = "O"
                score = self.minimax(self.board, depth+1, False)
                self.board[positions] = " "
                best_score = max(best_score, score)
            
            return best_score
        
        else:
            best_score = float("inf")
            possibilites = list(map(self.check_availability, [list(self.board.keys())]))[0]
            for positions in possibilites:
                self.board[positions] = "X"
                score = self.minimax(self.board, depth+1, True)
                self.board[positions] = " "
                best_score = min(best_score, score)
            
            return best_score

    def game_state_check(self, minimaxing:bool = False):

        self.update_board()
        for lines in self.winning_scenerio:
            if self.board[lines[0]] == self.board[lines[1]] == self.board[lines[2]] and self.board[lines[0]] != " ":
                if not minimaxing:
                    thread = threading.Thread(target=self.game_over, args=[{self.board[lines[0]]}])
                    thread.start()
                    return 
                else:
                    return self.scores[self.board[lines[0]]]

        if all(list(map(lambda x: x.strip(), self.board.values()))):
            self.update_board()
            if not minimaxing:
                thread = threading.Thread(target=self.game_over, args=["tie"])
                thread.start()
                return
            
            return 0
        
        return None

    def game_over(self, winner:str):
        self.ui.root.attributes('-disabled', True)
        # self.update_board()
        if not winner == "tie":
            print(1)
            alert(text=f"Game Over! {winner} wins!", title="Game Over", button="OK")
        
        else:
            alert(text="Game Over! Match Tied!", title="Game Over", button="OK")
        
        os._exit(0)

tester = GameState()

tester.ui.root.mainloop()