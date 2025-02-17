import tkinter as tk
from tkinter import ttk
import random

BOARD_ROWS = 6
BOARD_COLS = 7
cells = 70
canvas_width = cells * BOARD_COLS
canvas_height = cells * BOARD_ROWS
MAX_DEPTH = 4


root = tk.Tk()
root.title("Connect 4")


# Display name later
name = tk.StringVar()
scolor = ""
ocolor = ""
current_player = None
color_count = 0
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]




def start_game():
    global current_player, scolor
    save_name()
    current_player = name.get()  
    for widget in root.winfo_children():
        widget.destroy()
    draw_board()




def set_color(color):
    global scolor, ocolor, color_count
    if color_count == 0:
        scolor = color
        color_count += 1
    elif color_count == 1:
        ocolor = color
        color_count += 1





def draw_token(canvas, row, col):
    x_center = col * cells + cells // 2
    y_center = row * cells + cells // 2
    color = scolor if board[row][col] == name.get() else ocolor
    canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, outline=color, width=5)






def make_move(event, canvas):
    global current_player
    x = event.x
    col = x // cells

    for r in range(BOARD_ROWS - 1, -1, -1):
        if board[r][col] == '':
            board[r][col] = current_player
            draw_token(canvas, r, col)
            canvas.update()  
            if check_winner(current_player):
                winner()
                return
            elif draw_game():
                draw()
                return
            else:
                current_player = "Computer" if current_player == name.get() else name.get()
                if current_player == "Computer":
                    comp_move = best_move(board)
                    if comp_move is not None:
                        for r in range(BOARD_ROWS - 1, -1, -1):
                            if board[r][comp_move] == '':
                                board[r][comp_move] = "Computer"
                                draw_token(canvas, r, comp_move)
                                canvas.update()  
                                if check_winner("Computer"):
                                    winner()
                                    return
                                elif draw_game():
                                    draw()
                                    return
                                current_player = name.get()
                                break
            break
        



    # having the computer choose a random move instead of minimax since minimax seems to be the issue
    # test to make sure everything other than minimax works
def make_move_random(event, canvas):
    global current_player
    x = event.x
    col = x // cells

    for r in range(BOARD_ROWS - 1, -1, -1):
        if board[r][col] == '':
            board[r][col] = current_player
            draw_token(canvas, r, col)
            canvas.update() 
            if check_winner(current_player):
                winner()
                return
            elif draw_game():
                draw()
                return
            else:
                current_player = "Computer" if current_player == name.get() else name.get()
                if current_player == "Computer":
                    comp_move = rando_move(board)
                    if comp_move is not None:
                        for r in range(BOARD_ROWS - 1, -1, -1):
                            if board[r][comp_move] == '':
                                board[r][comp_move] = "Computer"
                                draw_token(canvas, r, comp_move)
                                #canvas.update()  
                                if check_winner("Computer"):
                                    winner()
                                    return
                                elif draw_game():
                                    draw()
                                    return
                                current_player = name.get()
                                break
            break


# random move generator for comp
def rando_move(board):
    rando = [col for col in range(BOARD_COLS) if board[0][col] == '']
    if rando:
        return random.choice(rando)
    return None




def save_name():
    global name
    name.set(name_entry.get())
        


def draw_game():
    return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))
    #    return True
    #return False




#might need to change up a lot of current functions
def minimax(board, depth, alpha, beta, max_player):
    if check_winner("Computer"):
        return 1
    elif check_winner(name.get()):
        return -1
    elif draw_game() or depth == MAX_DEPTH:
        return 0
    
    if max_player == True:
        best_score = float('-inf')
        # find a way to loop through each empty space in board
        # this is going to have to be re-written as a nested for loop or smt
        for col in range(BOARD_COLS):
            # start from bottom
            for row in range(BOARD_ROWS - 1, -1, -1):
                if board[row][col] == '':
                    board[row][col] = "Computer"
                    #draw_token(canvas, row, col)
                    #make_move(event, canvas)
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = ''
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    
    else:
        best_score = float('inf')
        #find a way to loop through each empty space in board
        # this is going to have to be re-written as a nested for loop or smt
        for col in range(BOARD_COLS):
            for row in range(BOARD_ROWS - 1, -1, -1):
                if board[row][col] == '':
                    board[row][col] = name.get()
                    #draw_token(canvas, row, col)
                    #make_move(event, canvas)
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = ''
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score
    



# loop through all cols and find empty cells and do minimax() and get that score, return the best score
def best_move(board):
    best_score = float('-inf')
    best = None
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS):
            if board[row][col] == '':
                board[row][col] = "Computer"
                score = minimax(board, 0, float('-inf'), float('inf'), False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best = col
    return best





# Update check_winner(player) to return true if player turn and player winner
# Do this by checking if the pieces in row are the current_player's color or not
# So if 4 in a row but not the curr_p's color --> lose, if it is the curr_p's color --> win
def check_winner(player):
    # Hotdog
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Hamburger
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Diagonal 1
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Diagonal 2
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

    


name_label = tk.Label(root, text="Enter your name:")
name_entry = tk.Entry(root, textvariable=name)
#name_field = tk.Entry(root, bg="SeaGreen1")

name_label.pack(padx=10, pady=10)
name_entry.pack(padx=10, pady=10)
#name_field.pack(padx=5, pady=5)


color_label = tk.Label(root, text="Choose what color you wish to play as: \n The first click is your's and the second is the computer. ")
color_label.pack(padx=10, pady=10)


lavender_button = tk.Button(root, font=('arial', 15, 'bold'), text="Lavender", bg="black", fg="purple", command=lambda: set_color("purple"))
lavender_button.pack(padx=5, pady=5)

blue_button = tk.Button(root, font=('arial', 15, 'bold'), text="Blue", bg="black", fg="blue", command=lambda: set_color("blue"))
blue_button.pack(padx=5, pady=5)

pink_button = tk.Button(root, font=('arial', 15, 'bold'), text="Pink", bg="black", fg="red", command=lambda: set_color("red"))
pink_button.pack(padx=5, pady=5)

white_button = tk.Button(root, font=('arial', 15, 'bold'), text="White", bg="black", fg="black", command=lambda: set_color("black"))
white_button.pack(padx=5, pady=5)

start_button = tk.Button(root, font=('arial', 15, 'bold'), text="Start Game", bg="black", fg="green", command=start_game)
start_button.pack(padx=10, pady=10)


def winner():
    if current_player == "Computer":
        winner_label = tk.Label(root, text=f"Computer Wins", font=('arial', 20, 'bold'))
    elif current_player != "Computer":
        winner_label = tk.Label(root, text=f"{name.get()} wins!", font=('arial', 20, 'bold'))
    winner_label.pack(pady=20)
    


def draw():
    winner_label = tk.Label(root, text=f"DRAW GAME", font=('arial', 20, 'bold'))
    winner_label.pack(pady=20)



def draw_board():
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="ivory2")


    for i in range(1, BOARD_ROWS):
        canvas.create_line(0, i * cells, canvas_width, i * cells, fill="black", width=5)

    for j in range(1, BOARD_COLS):
        canvas.create_line(j * cells, 0, j * cells, canvas_height, fill="black", width=5)
        
    canvas.bind("<Button-1>", lambda event: make_move(event, canvas))







root.configure(bg='sky blue')
root.mainloop()