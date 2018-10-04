import sys
from math import hypot
from itertools import cycle
from playsound import playsound

from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Move-tac-toe")
root.resizable(False, False)
frame = Frame(root, width=800, height=700)
frame.pack()
canvas = Canvas(frame, width=620, height=600, bg="white")
canvas.pack(side=BOTTOM)
WIDTH = HEIGHT = 600
GAP = 50
ONE_TIME_CONSTANT = 1
ALLOW_SINGLE_CLICK = 1
xRelease, yRelease = None, None
from_y = from_x = None
picked = 0

POINTS = [
    (GAP, GAP), (WIDTH//2, GAP), (WIDTH-GAP, GAP),
    (GAP, HEIGHT//2), (WIDTH//2, HEIGHT//2), (WIDTH-GAP, HEIGHT//2),
    (GAP, HEIGHT-GAP), (WIDTH//2, HEIGHT-GAP), (WIDTH-GAP, HEIGHT-GAP),
]

VALID_MOVES = {
    0: (1, 3, 4), 1: (0, 2, 4), 2: (1, 4, 5),
    3: (0, 4, 6), 4: (0, 1, 2, 3, 5, 6, 7, 8), 5: (4, 2, 8),
    6: (4, 3, 7), 7: (4, 6, 8), 8: (4, 5, 7)
}

GRID_POINTS = {
    0: (GAP, GAP, WIDTH-GAP, GAP),
    1: (GAP, HEIGHT/2, WIDTH-GAP, HEIGHT/2),
    2: (GAP, HEIGHT-GAP, WIDTH-GAP, HEIGHT-GAP),
    3: (WIDTH/2, GAP, WIDTH/2, HEIGHT-GAP),
    4: (WIDTH-GAP, GAP, WIDTH-GAP, HEIGHT-GAP),
    5: (GAP, GAP, WIDTH-GAP, HEIGHT-GAP),
    6: (GAP, HEIGHT-GAP, WIDTH-GAP, GAP),
    7: (GAP, GAP, GAP, HEIGHT-GAP)
}


class Player:

    def __init__(self, name, color_notation):
        self.name = name
        self.color_notation = color_notation
        self.owned_position = {}
        self.remaining_piece = 3


def draw_grid():
    for i in range(8):
        canvas.create_line(GRID_POINTS[i][0], GRID_POINTS[i][1], GRID_POINTS[i][2],
                           GRID_POINTS[i][3], width=4)


def get_nearest_node(x, y):
    temp = sys.maxsize
    for i in range(9):
        distance = hypot(x-POINTS[i][0], y-POINTS[i][1])
        if distance < temp:
            temp = distance
            nearest_point = (POINTS[i][0], POINTS[i][1])
    if temp > 40:
        return None, None
    return nearest_point


def own_cell(x, y, player):
    if (x, y) in player.owned_position.values():
        return 1


def get_oval_obj_key(x, y, player):
    for key, val in player.owned_position.items():
        if val == (x, y):
            return key


def is_empty(x, y):
    if player_1.owned_position or player_2.owned_position:
        if (x, y) in player_1.owned_position.values() or (x, y) in player_2.owned_position.values():
            return 0
    return 1


def all_filled():
    if (player_1.remaining_piece) == (player_2.remaining_piece) == 0:
        return 1


def is_movable(a, b):
    current_index = POINTS.index((a, b))
    for i in VALID_MOVES[current_index]:
        x, y = POINTS[i]
        if is_empty(x, y):
            return 1
    return 0


def can_move_piece():
    info['text'] = ""
    if player_1.remaining_piece == 0 and player_2.remaining_piece == 0:
        return 1


def valid_move_has_empty_cell(tupp):
    for i in tupp:
        x, y = POINTS[i]
        if is_empty(x, y):
            return True
    return False


def legal_move(x, y, x_prev=None, y_prev=None):
    if x_prev == x and y_prev == y:
        return True
    current_index = POINTS.index((x, y))
    previous_index = POINTS.index((x_prev, y_prev))
    if current_index in VALID_MOVES[previous_index]:
        return True
    info['text'] = "Invalid Move  "
    return False


def check_moving_condition(a, b, x_prev, y_prev):
    return a is not None and x_prev is not None and is_empty(a, b) and legal_move(a, b, x_prev, y_prev)


def bring_oval_in_motion(event, obj_index):
    canvas.coords(obj_index, event.x-30, event.y-30, event.x+30, event.y+30)


def stop_floating_obj(from_x, from_y, current_player):
    canvas.unbind("<Motion>")
    index_of_obj = get_oval_obj_key(from_x, from_y, current_player)
    canvas.coords(index_of_obj, from_x - 30, from_y - 30, from_x + 30,
                  from_y + 30)
    return 0


def move_a_piece(a, b, x_prev, y_prev):
    oval_obj = canvas.create_oval(a-30, b-30, a+30, b+30, fill=current_player.color_notation)
    canvas.delete(get_oval_obj_key(x_prev, y_prev, current_player))
    current_player.owned_position.pop(get_oval_obj_key(x_prev, y_prev, current_player), None)
    current_player.owned_position[oval_obj] = (a, b)


def toggle_turn():
    global current_player
    current_player = players.__next__()
    status['text'] = "  Turn: " + current_player.color_notation


def fill_pieces(a, b, current_player):
    oval_obj = canvas.create_oval(a-30, b-30, a+30, b+30, fill=current_player.color_notation)
    playsound("filling.wav")
    current_player.owned_position[oval_obj] = (a, b)
    current_player.remaining_piece -= 1
    if check_game():
        show_result()
        return 1
    toggle_turn()


def float_piece(from_x, from_y, current_player):
    index_of_obj = get_oval_obj_key(from_x, from_y, current_player)
    canvas.bind("<Motion>", lambda event: bring_oval_in_motion(event, index_of_obj))
    return 1


def move_pieces(a, b, from_x, from_y):
    canvas.unbind("<Motion>")
    playsound("moving.wav")
    move_a_piece(a, b, from_x, from_y)
    if check_game():
        show_result()
        return 0
    toggle_turn()


def is_valid_cord(a):
    if a is None:
        return 0


def prevent_function(a, b, current_player):
    if not is_movable(a, b):
        info['text'] = "Immovable"
        return 1
    if not own_cell(a, b, current_player):
        return 1


def is_invalid_drop(a, b, picked):
    return a is None or ((a is None  or not is_empty(a, b)) and can_move_piece() and picked == 1)


def bypass_release_once(button_release):
    return not can_move_piece() and button_release == False


def move(event, button_release):
    global from_y, from_x, picked, current_player
    a, b = get_nearest_node(event.x, event.y)

    if bypass_release_once(button_release):
        return
    if is_invalid_drop(a, b, picked):
        picked = stop_floating_obj(from_x, from_y, current_player)
        return
    if not can_move_piece():
        if not all_filled() and is_empty(a, b) and button_release:
            fill_pieces(a, b, current_player)

    else:

        if button_release == False and not is_empty(a, b):

            from_x, from_y = get_nearest_node(event.x, event.y)
            if prevent_function(from_x, from_y, current_player):
                picked = 0
            else:
                picked = float_piece(from_x, from_y, current_player)

        elif button_release:

            a, b = get_nearest_node(event.x, event.y)
            if picked != 1:
                return
            if check_moving_condition(a, b, from_x, from_y):
                picked = move_pieces(a, b, from_x, from_y)
            else:
                picked = stop_floating_obj(from_x, from_y, current_player)


def check_game():
    global current_player
    coordinates = tuple(current_player.owned_position.values())
    if len(coordinates) != 3:
        return 0
    x1, y1 = coordinates[0][0], coordinates[0][1]
    x2, y2 = coordinates[1][0], coordinates[1][1]
    x3, y3 = coordinates[2][0], coordinates[2][1]
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)


def help_game():
    messagebox.showinfo("Help", "Welcome to the movable tic-tac-toe game. "
                                "The playing rules and win conditions are same "
                                "as that of Tic-Tac-Toe game except the limitation of number of pieces. "
                                "Each player has 3 pieces and after s/he has put all the "
                                "pieces in the board, s/he should drag the pieces. "
                                "Single click to put the piece in the board and double click to drag. "
                                "Double click on the position again to place the dragged piece. ")


def close():
    root.destroy()


def show_result():
    print("Game won by ", current_player.color_notation)
    status['text'] = "Game Over!  " + current_player.color_notation + " won the game"
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<ButtonRelease-1>")
    messagebox.showinfo("Game Over!!! ", current_player.color_notation + " won the game")


player_1 = Player("Sudarshan", "Blue")
player_2 = Player("Barna", "Red")
players = cycle([player_1, player_2])
info = Label(root, text="", font="Times 12 bold")
info.pack(side=RIGHT)
status = Label(root, text="  Turn:  " + player_1.color_notation , font="Times 12 bold", padx=0, pady=5, bd=6)
status.pack(side=LEFT, fill=X)


def new_game():
    canvas.delete(ALL)
    draw_grid()
    status['text'] = ""
    canvas.bind('<ButtonPress-1>', lambda event: move(event, False))
    canvas.bind('<ButtonRelease-1>', lambda event: move(event, True))
    player_1.remaining_piece = player_2.remaining_piece = 3
    player_1.owned_position = {}
    player_2.owned_position = {}


new_game()
toggle_turn()

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu =  Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Game", command=new_game)
file_menu.add_command(label="Exit", command=close)
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_command(label="Instructions", command=help_game)

root.mainloop()
