import os
import threading

from collections import deque
from pyautogui import alert
from copy import deepcopy
from gui import GUI
        

class Game:
    """The main class that handles the GAME"""
    def __init__(self) -> None:
        self.ui = GUI() # creating an instance of the GUI class 

        # winning scenarios
        self.winning_scenarios = [
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

        self.history = [] # history of the board.

        self.current_player = "X" # the player that goes first

        # scores for different game ending scenarios for minimax algorithm
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
    
    def board_snapshot(self, x_queue:deque, o_queue:deque) -> tuple[tuple[tuple[int]]]:
        """Returns the current snapshot of the board."""
        return (tuple(x_queue), tuple(o_queue))

    def button_handler(self, position:tuple[int], button) -> None:
        """Function responsible for handling the button presses"""

        self.play(self.board, self.Player_X_queue, self.Player_O_queue, position) # making the play
        button.config(state = "disabled") # disabling the buttons that were pressed
        self.update_board() # updating the boards
        self.game_state_check(self.board) # checking whether the game has ended or not

    def play(self, board:dict, Player_X_queue:deque, Player_O_queue:deque, position:tuple[int], simulating:bool = False, current_player:str | None = None) -> dict[tuple[int]:str]:
        """Function responsible for handling the plays made by the players."""

        if not current_player:
            if self.current_player == "X": # if the Player_X has made the move

                if len(Player_X_queue) < 3: # if the player has made 3 or less moves on the board
                    Player_X_queue.append(position) # append the move by the player to its queue

                else:
                    removed = Player_X_queue.popleft() # remove the oldest move by the player from the queue
                    board[removed] = " " # empty the spot 
                    if not simulating:
                        self.button_position[removed].config(state="active") # reactivate the button
                    Player_X_queue.append(position) # append the new move by the player to the queue
                
                if board[position] == " ": # modifying the board only when the place was empty
                    board[position] = self.current_player

                if not simulating:
                    self.current_player = "O" # switching the current player
                    self.computer_turn() # initiating the computer's turn

            else: # if the Player_O has made the move

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
                
                if not simulating:
                    self.current_player = "X" # changing the current player

            return board, Player_X_queue, Player_O_queue

        else:
            if current_player == "X": # if the Player_X has made the move

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

                if not simulating:
                    current_player = "O" # switching the current player
                    self.computer_turn() # initiating the computer's turn

            else: # if the Player_O has made the move

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

        # hardcoding standard scenarios to improve the time.
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

        possibilities = list(map(self.check_availability, [self.board], [list(self.board.keys())]))[0] # getting the possible unoccupied places.
        
        if possibilities: # if the board is still empty.
            for positions in possibilities:
                # creating a deepcopy of the board and the queues
                board = deepcopy(self.board) # creating the copy of self.board to prevent modifying the original one.
                Player_X_queue = deepcopy(self.Player_X_queue)
                Player_O_queue = deepcopy(self.Player_O_queue)

                # simulating the plays
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
            return winner # return the score of the scenario.

        possibilities = list(map(self.check_availability,  [board], [list(board.keys())]))[0] # getting the position of the available spots on the board

        # setting max depth based on the number of empty spots on the board.
        if len(possibilities) >= 6:
            max_depth = 8
        else:
            max_depth = 5

        if depth > max_depth:
            best_score = self.scenario_checker(board) # initiating the scenario checker function when the depth has been reached.
            return best_score
        
        else:
            if isMaximizing: # if we are supposed to maximize.
                best_score = float("-inf") # initial score for maximizing.

                for positions in possibilities: 
                    # creating a deepcopy of the board and the queues

                    new_board = deepcopy(board)
                    new_xq = deepcopy(Player_X_queue)
                    new_oq = deepcopy(Player_O_queue)

                    board_recursed, new_xq, new_oq = self.play(new_board, new_xq, new_oq, positions, simulating=True, current_player="O")
                    score = self.minimax(board_recursed, new_xq, new_oq, depth+1, False, alpha, beta)

                    best_score = max(best_score, score)
                    # implementing alpha beta pruning.
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break 
                
                return best_score # returning the best possible score calculated based on the given scenario of the board. 
            
            else: # if we are supposed to minimize.

                best_score = float("inf") # initial score for minimizing.
                for positions in possibilities:
                    # creating a deepcopy of the board and the queues
                    new_board = deepcopy(board)
                    new_xq = deepcopy(Player_X_queue)
                    new_oq = deepcopy(Player_O_queue)

                    board_recursed, new_xq, new_oq = self.play(new_board, new_xq, new_oq, positions, simulating=True, current_player="X")
                    score = self.minimax(board_recursed, new_xq, new_oq, depth+1, True, alpha, beta)

                    best_score = min(best_score, score)
                    # implementing alpha beta pruning.
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # prune branch
                
                return best_score # returning the best score.

    def scenario_checker(self, board:dict[tuple[int]:str]) -> int:
        """Heuristic function responsible for giving score to a certain game scenario"""
        score = 0 # iniitial score.
        for line in self.winning_scenarios:
            ai_count = sum(board[posn] == "O" for posn in line)
            opp_count = sum(board[posn] == "X" for posn in line)

            if ai_count > 0 and opp_count == 0:
                # giving points when the ai has one more elements in a winning like and the opponent has none.
                score += 10 ** ai_count
            elif opp_count > 0 and ai_count == 0:
                # deductting points for the opposite case.:
                score -= 10 ** opp_count

        if board[(1,1)] == "O":
            score += 5 # center is occupied by the ai
        elif board[(1,1)] == "X":
            score -= 5 # center is occupied by the human

        return score

    def game_state_check(self, board:dict, minimaxing:bool = False) -> int | None:
        """Responsible for checking the state of the board."""

        # checking for the winning scenario
        for lines in self.winning_scenarios:

            if board[lines[0]] == board[lines[1]] == board[lines[2]] and board[lines[0]] != " ":
                
                if not minimaxing: # if not executed through the minimax algorithm.
                    thread = threading.Thread(target=self.game_over, args=[board[lines[0]]]) # start the game over thread.
                    thread.start()
                    return 
                
                else:
                    return self.scores[board[lines[0]]] # return the score of the scenario.

        if not minimaxing:
            snapshot = self.board_snapshot(self.Player_X_queue, self.Player_O_queue)
            self.history.append(snapshot)

            if self.history.count(snapshot) >= 3:
                thread = threading.Thread(target=self.game_over, args=["tie"]) # starting the game over thread.
                thread.start()
                return
        
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
    game = Game()
    game.ui.root.mainloop() # running the game.