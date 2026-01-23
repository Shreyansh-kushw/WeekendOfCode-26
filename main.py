import os
import threading

from tkinter import *
from collections import deque
from pyautogui import alert
from copy import deepcopy

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
        self.btn00 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn00.config(height = 2, width = 4)
        self.btn00.grid(column = 0, row = 0)

        self.btn01 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn01.config(height = 2, width = 4)
        self.btn01.grid(column = 15, row = 0)

        self.btn02 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn02.config(height = 2, width = 4)
        self.btn02.grid(column = 30, row = 0)

        self.btn10 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn10.config(height = 2, width = 4)
        self.btn10.grid(column = 0, row = 10)

        self.btn11 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn11.config(height = 2, width = 4)
        self.btn11.grid(column = 15, row = 10)

        self.btn12 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn12.config(height = 2, width = 4)
        self.btn12.grid(column = 30, row = 10)

        self.btn20 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn20.config(height = 2, width = 4)
        self.btn20.grid(column = 0, row = 20)

        self.btn21 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn21.config(height = 2, width = 4)
        self.btn21.grid(column = 15, row = 20)

        self.btn22 = Button(self.square_frame, text ="", bg = "white", font=("Arial", 36))
        self.btn22.config(height = 2, width = 4)
        self.btn22.grid(column = 30, row = 20)
        

class Game:
    """The main class that handles the GAME"""
    def __init__(self) -> None:
        self.ui = GUI() # creating an instance of the GUI class 

        # winning scenerios
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

        # the board
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

        # dictionary relating the buttons to their respective positions
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
        
        # updating the board        
        self.update_board()
        
        # creating the queues for the turns taken by the players
        self.Player_X_queue = deque()
        self.Player_O_queue = deque()

        self.current_player = "X" # the player that goes first

        # scores for different game ending scenerios for minimax algorithm
        self.scores = {
            "X" : -1000,
            "O" : 1000,
            "tie" : 0,
        }

    def update_board(self) -> None:
        """Function responsible for updating the board"""

        self.ui.btn00.config(text=self.board[(0,0)], command= lambda: self.button_handler((0,0), self.button_position[(0,0)]))
        self.ui.btn01.config(text=self.board[(0,1)], command= lambda: self.button_handler((0,1), self.button_position[(0,1)]))
        self.ui.btn02.config(text=self.board[(0,2)], command= lambda: self.button_handler((0,2), self.button_position[(0,2)]))
        self.ui.btn10.config(text=self.board[(1,0)], command= lambda: self.button_handler((1,0), self.button_position[(1,0)]))
        self.ui.btn11.config(text=self.board[(1,1)], command= lambda: self.button_handler((1,1), self.button_position[(1,1)]))
        self.ui.btn12.config(text=self.board[(1,2)], command= lambda: self.button_handler((1,2), self.button_position[(1,2)]))
        self.ui.btn20.config(text=self.board[(2,0)], command= lambda: self.button_handler((2,0), self.button_position[(2,0)]))
        self.ui.btn21.config(text=self.board[(2,1)], command= lambda: self.button_handler((2,1), self.button_position[(2,1)]))
        self.ui.btn22.config(text=self.board[(2,2)], command= lambda: self.button_handler((2,2), self.button_position[(2,2)]))
    
    def button_handler(self, position:tuple[int], button:Button) -> None:
        """Function responsible for handling the button presses"""

        self.play(self.board, self.Player_X_queue, self.Player_O_queue, position) # making the play
        button.config(state = "disabled") # disabling the buttons that were pressed
        self.update_board() # updating the boards
        self.game_state_check(self.board) # checking whether the game has ended or not

    def play(self, board:dict, Player_X_queue:deque, Player_O_queue:deque, position:tuple[int], simulating:bool = False, current_player:str | None = None) -> dict:
        """Function responsible for handling the plays made by the players."""

        if not current_player:
            if self.current_player == "X": # if the Player_X has made the move

                # Player_X_queue.append(position)
                if len(Player_X_queue) < 3:
                    Player_X_queue.append(position)

                else:
                    removed = Player_X_queue.popleft()
                    board[removed] = " "
                    if not simulating:
                        self.button_position[removed].config(state="active")
                    Player_X_queue.append(position)
                
                if board[position] == " ": # modifying the board only when the place was empty
                    board[position] = self.current_player

                else:
                    pass
                
                if not simulating:
                    self.current_player = "O" # switching the current player
                    self.computer_turn() # initiating the computer's turn
                # return board, Player_X_queue, Player_O_queue
            else: # if the Player_O has made the move

                # Player_O_queue.append(position)
                if len(Player_O_queue) < 3:
                    Player_O_queue.append(position)

                else:
                    removed = Player_O_queue.popleft()
                    board[removed] = " "
                    if not simulating:
                        self.button_position[removed].config(state="active")
                    Player_O_queue.append(position)
                
                if board[position] == " ": # modifying the board only when the place is empty
                    board[position] = self.current_player 
                
                else:
                    pass
                
                if not simulating:
                    self.current_player = "X" # changing the current player
            return board, Player_X_queue, Player_O_queue
        else:
            if current_player == "X": # if the Player_X has made the move

                # Player_X_queue.append(position)
                if len(Player_X_queue) < 3:
                    Player_X_queue.append(position)

                else:
                    removed = Player_X_queue.popleft()
                    board[removed] = " "
                    if not simulating:
                        self.button_position[removed].config(state="active")
                    Player_X_queue.append(position)
                
                if board[position] == " ": # modifying the board only when the place was empty
                    board[position] = current_player

                else:
                    pass
                
                if not simulating:
                    current_player = "O" # switching the current player
                    self.computer_turn() # initiating the computer's turn
                # return board, Player_X_queue, Player_O_queue
            else: # if the Player_O has made the move

                # Player_O_queue.append(position)
                if len(Player_O_queue) < 3:
                    Player_O_queue.append(position)

                else:
                    removed = Player_O_queue.popleft()
                    board[removed] = " "
                    if not simulating:
                        self.button_position[removed].config(state="active")
                    Player_O_queue.append(position)
                
                if board[position] == " ": # modifying the board only when the place is empty
                    board[position] = current_player 
                
                else:
                    pass
                
                if not simulating:
                    current_player = "X" # changing the current player
            return board, Player_X_queue, Player_O_queue

    def check_availability(self, board, keys:list[tuple[int]]) -> list:
        """Returns the list of all the unoccupied positions on the board."""

        new_list = []

        for key in keys:
            if board[key] != " ":
                pass
            else:
                new_list.append(key)  
        
        return new_list

    def computer_turn(self) -> None:
        """Responsible for handling the moves made by the computer."""

        self.ui.root.attributes('-disabled', True) # disabling the interactions with the tkinter window till the computer decides its move

        # hardcoding standard scenerios to improve the time.
        if self.board[(1,1)] == " " and list(self.board.values()).count(" ") == 8: # When the human plays anywhere other than the center as his first move
            self.button_handler((1,1), self.button_position[(1,1)]) # play at the center
            self.ui.root.attributes('-disabled', False) # re-enabling the tkinter window after the computer has played its turn
            return
        
        elif self.board[(1,1)] == "X" and list(self.board.values()).count(" ") == 8: # when the human plays at the center in his first move.
            self.button_handler((0,0), self.button_position[(0,0)]) # play at any corner
            self.ui.root.attributes('-disabled', False) # re-enabling the tkinter window after the computer has played its turn
            return

        # Minimax algorithm
        best_score = float("-inf") # initial score for maximizing.

        possibilites = list(map(self.check_availability, [self.board], [list(self.board.keys())]))[0] # getting the possible unoccupied places.
        
        if possibilites: # if the board is still empty.
            for positions in possibilites:
                board = deepcopy(self.board) # creating the copy of self.board to prevent modifying the original one.
                Player_X_queue = deepcopy(self.Player_X_queue)
                Player_O_queue = deepcopy(self.Player_O_queue)

                board_recursed, Player_X_queue, Player_O_queue = self.play(board, Player_X_queue, Player_O_queue, positions, simulating=True)
                score = self.minimax(board_recursed, Player_X_queue, Player_O_queue, 0, False)
                if score > best_score:
                    best_score = score
                    best_move = positions

            self.button_handler(best_move, self.button_position[best_move]) # executing the best move.
        
        else: # if the board has no empty boxes.
            self.game_state_check(board) # check the state of the game
        self.ui.root.attributes('-disabled', False) # re-enabling the tkinter window after the computer has played its turn

    def minimax(self, board, Player_X_queue, Player_O_queue, depth:int = 0, isMaximizing:bool = True, alpha:float = -float("inf"), beta:float = float("inf")) -> float | int:
        """The main minimax algorithm"""

        winner = self.game_state_check(board, minimaxing=True) # checking for the state of the game before running the whole algo.
        if winner is not None: #  if the game has ended. ie there is a winner/tie.
            return winner # return the score of the scenerio.
        if depth > 10:
            best_score = self.scenerio_checker(board)
            return best_score
        
        else:
            if isMaximizing: # if we are supposed to maximize.
                best_score = float("-inf") # initial score for maximizing.
                possibilites = list(map(self.check_availability,  [board], [list(board.keys())]))[0] # getting the available spots.

                # maximizing algorithm
                for positions in possibilites: 
                    new_board = deepcopy(board)
                    new_xq = deepcopy(Player_X_queue)
                    new_oq = deepcopy(Player_O_queue)

                    board_recursed, new_xq, new_oq = (self.play(new_board, new_xq, new_oq, positions, simulating=True, current_player= "O"))
                    score = self.minimax(board_recursed, new_xq, new_oq, depth+1, False, alpha, beta)
                    # board[positions] = " "``
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break 
                
                return best_score # returning the best possible score calculated based on the given scenerio of the board. 
            
            else: # if we are supposed to minimize.

                best_score = float("inf") # initial score for minimizing.
                possibilites = list(map(self.check_availability,  [board], [list(board.keys())]))[0]
                for positions in possibilites:
                    new_board = deepcopy(board)
                    new_xq = deepcopy(Player_X_queue)
                    new_oq = deepcopy(Player_O_queue)

                    board_recursed, new_xq, new_oq = (self.play(new_board, new_xq, new_oq, positions, simulating=True, current_player="X"))
                    score = self.minimax(board_recursed, new_xq, new_oq, depth+1, True, alpha, beta)
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # prune branch
                
                return best_score # returning the best score.

    def scenerio_checker(self, board):
        score = 0
        print("checking scenerio")
        for line in self.winning_scenerio:
            ai_count = sum(board[posn] == "O" for posn in line)
            opp_count = sum(board[posn] == "X" for posn in line)

            if ai_count > 0 and opp_count == 0:
                score += 10 ** ai_count
            elif opp_count > 0 and ai_count == 0:
                score -= 10 ** opp_count

        if board[(1,1)] == "O":
            score += 5
        elif board[(1,1)] == "X":
            score -= 5

        return score

    def game_state_check(self, board:dict, minimaxing:bool = False) -> int | None:
        """Responsible for checking the state of the board."""

        # checking for the winning scenerio
        for lines in self.winning_scenerio:

            if board[lines[0]] == board[lines[1]] == board[lines[2]] and board[lines[0]] != " ":
                
                if not minimaxing: # if not executed thru the minimax algorithm.
                    thread = threading.Thread(target=self.game_over, args=[{board[lines[0]]}]) # start the game over thread.
                    thread.start()
                    return 
                
                else:
                    return self.scores[board[lines[0]]] # return the score of the scenerio.

        if all(list(map(lambda x: x.strip(), board.values()))): # if the whole board is filled.

            if not minimaxing:
                thread = threading.Thread(target=self.game_over, args=["tie"]) # starting the game over thread.
                thread.start()
                return
            
            return 0 # score for the tie scenerio
        
        return None

    def game_over(self, winner:str):
        """Function handling the generation of the dialog box upon game over."""

        self.ui.root.attributes('-disabled', True) # disabling the tkinter window. 

        if not winner == "tie": # if the game is not a tie.
            alert(text=f"Game Over! {winner} wins!", title="Game Over", button="OK")
        
        else: # if the game is tied.
            alert(text="Game Over! Match Tied!", title="Game Over", button="OK")
        
        os._exit(0)

if __name__ == "__main__":

    tester = Game()
    tester.ui.root.mainloop() # running the game.