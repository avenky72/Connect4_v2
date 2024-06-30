import tkinter as tk
from tkinter import ttk

BOARD_ROWS = 6
BOARD_COLS = 7
cells = 70
canvas_width = cells * BOARD_COLS
canvas_height = cells * BOARD_ROWS

root = tk.Tk()
root.title("Connect 4")


# Display name later
name = tk.StringVar()
scolor = ""
current_player = 'X'
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]




def start_game():
    global scolor
    for widget in root.winfo_children():
        widget.destroy()

    draw_board()




def set_color(color):
# Set background color based on user's choise
    global scolor
    scolor = color


def draw_mark(canvas, row, col):
    x_center = col * cells + cells // 2
    y_center = row * cells + cells // 2
    if current_player == 'X':
        canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, outline=scolor, width=5)
    else:
        canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, outline="black", width=5)



def make_move(event, canvas):
    global current_player
    x, y = event.x, event.y
    col = x // cells
    
    for r in range(BOARD_ROWS - 1, -1, -1):
        if board[r][col] == '':
            board[r][col] = current_player
            draw_mark(canvas, r, col)
            if check_winner():
                winner()
            elif draw_game():
                draw()
            else:
                current_player = 'O' if current_player == 'X' else 'X'
            break
        
        
        

def draw_game():
    if not any('' in row for row in board) and not check_winner():
        return True
    return False


def check_winner():
    # Hotdog
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS - 3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] != '':
                return True

    # Hamburger
    for j in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] != '':
                return True

    # Diagonals
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLS - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] != '':
                return True
    
    return False
    

name_label = tk.Label(root, text="Enter your name:")
name_entry = tk.Entry(root, textvariable=name)
name_label.pack(padx=10, pady=10)
name_entry.pack(padx=10, pady=10)

color_label = tk.Label(root, text="Choose what color you wish to play as: ")
color_label.pack(padx=10, pady=10)


lavender_button = tk.Button(root, font=('arial', 15, 'bold'), text="Lavender", bg="black", fg="purple", command=lambda: set_color("plum1"))
lavender_button.pack(padx=5, pady=5)

blue_button = tk.Button(root, font=('arial', 15, 'bold'), text="Blue", bg="black", fg="blue", command=lambda: set_color("turquoise"))
blue_button.pack(padx=5, pady=5)

pink_button = tk.Button(root, font=('arial', 15, 'bold'), text="Pink", bg="black", fg="red", command=lambda: set_color("pink"))
pink_button.pack(padx=5, pady=5)

white_button = tk.Button(root, font=('arial', 15, 'bold'), text="White", bg="black", fg="black", command=lambda: set_color("white"))
white_button.pack(padx=5, pady=5)

start_button = tk.Button(root, font=('arial', 15, 'bold'), text="Start Game", bg="black", fg="green", command=start_game)
start_button.pack(padx=10, pady=10)


def winner():
    winner_label = tk.Label(root, text=f"Player {current_player} wins!", font=('arial', 20, 'bold'))
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