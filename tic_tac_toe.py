import pygame , math
pygame.init()

WIDTH , HEIGHT = 500 , 500
BLOCK_WIDTH , BLOCK_HEIGHT = WIDTH//3 , HEIGHT//3
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
BLACK = (0 , 0 , 0)
GREEN = (0 , 255 , 0)
WHITE = (255 , 255 , 255)
FPS = 30
font = pygame.font.SysFont('comicsans' , 60)

def isBoardFull(board):
    if board.count(' ')>1:
        return False
    else:
        return True

def drawBoard():
    WIN.fill(BLACK)

    #draw lines 
    for i in range(2):
        pygame.draw.line(WIN , GREEN , ((i+1)*BLOCK_WIDTH,0) , ((i+1)*BLOCK_WIDTH , HEIGHT) , width=2)
    for i in range(2):
        pygame.draw.line(WIN , GREEN , (0 , (i+1)*BLOCK_HEIGHT) , (WIDTH , (i+1)*BLOCK_HEIGHT) , width = 2)

    for i in range(1 , len(board)):
        surface = font.render(board[i] , 1 , WHITE)
        WIN.blit(surface , (((i - 1)%3)*BLOCK_WIDTH + (BLOCK_WIDTH - surface.get_width())//2, ((i-1)//3) * BLOCK_HEIGHT + (BLOCK_HEIGHT - surface.get_height())//2))

def display_text(text):
    WIN.fill(BLACK)
    surface = font.render(text , 1 , WHITE)
    WIN.blit(surface , ((WIDTH - surface.get_width())//2 , (HEIGHT - surface.get_height())//2))
    pygame.display.update()
    pygame.time.delay(1000)

def isWinner(board , le):
    return (board[1][0]==board[2][0]==board[3][0]==le) or (board[4][0]==board[5][0]==board[6][0]==le) or (board[7][0]==board[8][0]==board[9][0]==le) or (board[1][0]==board[4][0]==board[7][0]==le) or (board[2][0]==board[5][0]==board[8][0]==le) or (board[3][0]==board[6][0]==board[9][0]==le) or (board[1][0]==board[5][0]==board[9][0]==le)  or (board[3][0]==board[5][0]==board[7][0]==le)

def minimax(board , history , x_queue , o_queue , depth , isMaximizing):
    score = None
    if depth == 10 :
        return 0 
    if isWinner(board , 'X'):
        score = -1 
    elif isWinner(board , 'O'):
        score = 1
    elif isDraw(history , (x_queue + o_queue)):
        print("yes")
        score = 0
    
    if score != None:
        return score

    if isMaximizing :
        bestScore = -math.inf 
        vanishing_pos = None 
        for i in range(1 , len(board)):
            if bestScore == 1 :
                break 
            if board[i] == ' ':
                if len(o_queue) == 3 :
                    board[o_queue[0]] = ' '
                    vanishing_pos = o_queue.pop(0)
                board[i] = 'O' 
                o_queue.append(i)

                score = minimax(board , history , x_queue , o_queue , depth + 1, False)

                board[i] = ' '
                if vanishing_pos : 
                    o_queue.insert(0 , vanishing_pos)
                    board[vanishing_pos] = 'O'
                o_queue.pop()

                board[i] = ' '
                bestScore = max(bestScore, score)
    
    else :
        bestScore = math.inf 
        vanishing_pos = None 
        for i in range(1 , len(board)):
            if bestScore == -1 :
                break 
            if board[i] == ' ':
                if len(x_queue) == 3 :
                    board[x_queue[0]] = ' '
                    vanishing_pos = x_queue.pop(0)
                board[i] = 'X' 
                x_queue.append(i)     

                score = minimax(board , history , x_queue , o_queue , depth + 1, True)

                board[i] = ' '
                if vanishing_pos : 
                    x_queue.insert(0 , vanishing_pos)
                    board[vanishing_pos] = 'X'
                x_queue.pop()

                bestScore = min(bestScore, score)      
        
    return bestScore

def compMove(board , history , x_queue , o_queue):
    bestScore = -math.inf
    move = 0
    vanishing_pos = None
    for i in range(1 , len(board)):
        if board[i] == ' ' :
            if len(o_queue) == 3 :
                board[o_queue[0]] = ' '
                vanishing_pos = o_queue.pop(0)
            board[i] = 'O' 
            o_queue.append(i)

            score = minimax(board , history , x_queue , o_queue , 0 , False)

            board[i] = ' '
            if vanishing_pos :
                o_queue.insert(0 , vanishing_pos)
                board[vanishing_pos] = 'O'
            o_queue.pop()

            if score > bestScore :
                bestScore = score 
                move = i 
    
    return move 

def isDraw(history , track):
    return (history.count(track) == 3)

def main():
    clock = pygame.time.Clock()
    run = True 
    text = ''
    x_queue = []
    o_queue = []
    history = []

    while run and not(isDraw(history , (x_queue + o_queue))):
        clock.tick(FPS)

        paused = True 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not(isWinner(board , 'O')):
                paused = False 
                mouse_x , mouse_y = pygame.mouse.get_pos()
                pos = (mouse_x//BLOCK_WIDTH + 1) + mouse_y//BLOCK_HEIGHT * 3

                if board[pos] == ' ' :
                    if len(x_queue) == 3:
                        board[x_queue[0]] = ' '
                        x_queue.pop(0)
                    board[pos] = 'X' 
                    x_queue.append(pos) 

                else : 
                    paused = True         

            elif isWinner(board , 'O'):
                text = 'O Won !'
                run = False
                break 

            if not paused :
                if not(isWinner(board , 'X')):
                    move = compMove(board , history , x_queue , o_queue)
                    if move == 0 :
                        pass 
                    else:
                        if len(o_queue) == 3 :
                            board[o_queue[0]] = ' '
                            o_queue.pop(0)
                        board[move] = 'O' 
                        o_queue.append(move)
                        
                        if len(x_queue) == 3:
                            history.append(x_queue + o_queue)
                else :
                    text = 'X Won !'
                    run = False 
                    break 

        drawBoard()
        pygame.display.update()

    if isDraw(history , (x_queue + o_queue)):
        display_text("Tie Game !")
    else :
        display_text(text)

run = True 
while run :
    board = [' ' for x in range(10)]
    main()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False 
            pygame.quit()
            exit()