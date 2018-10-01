from sys import maxsize
from math import hypot
from itertools import cycle

from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Barna's board Game")
root.resizable(False, False)
frame = Frame(root, width=800, height=700)
frame.pack()
canvas = Canvas(frame, width=620, height=600, bg="white")
canvas.pack(side=BOTTOM)
WIDTH = HEIGHT = 600
GAP = 50
ONE_TIME_CONSTANT = 1
xprev = None
yprev = None
ALLOW_SINGLE_CLICK = 1
xRelease, yRelease = None, None

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


def draw_grid():
    for i in range(8):
        canvas.create_line(GRID_POINTS[i][0], GRID_POINTS[i][1], GRID_POINTS[i][2],
                           GRID_POINTS[i][3], width=3)


def result():
    print("Game won by ", current_player.color_notation)
    status['text'] = "Game Over!  " + current_player.color_notation + " wins the game"
    canvas.unbind("<Button-1>")
    canvas.unbind("<Double-Button-1>")
    messagebox.showinfo("Game Over!!! ", current_player.color_notation + " wins the game")


def get_nearest_node(x, y):
    nearest_point = 0  # just for the sake of satisfying PEP-8 convention, nearest point
    # wouldn't be referenced before assignment, because the if condition becomes true for
    # at least one condition
    temp = maxsize
    for i in range(9):
        distance = hypot(x-POINTS[i][0], y-POINTS[i][1])
        if distance < temp:
            temp = distance
            nearest_point = (POINTS[i][0], POINTS[i][1])
    if temp > 30:
        return None, None
    return nearest_point


def invalid_double_click(a, b, x_prev):
    return (a is None) or (x_prev is None and is_empty(a, b)) \
           or (len(player_1.owned_position) != 3 and len(player_2.owned_position) != 3)


def is_obj_movable(a, b, x_prev, player, allow_single_click):
    return (x_prev is None) and own_cell(a, b, player) and (allow_single_click == 0)


def check_moving_condition(a, b, x_prev, y_prev):
    return x_prev is not None and is_empty(a, b) and legal_move(a, b, x_prev, y_prev)


def move_a_piece(a, b, x_prev, y_prev):
    oval_obj = canvas.create_oval(a-30, b-30, a+30, b+30, fill=current_player.color_notation)
    canvas.delete(get_oval_obj_key(x_prev, y_prev, current_player))
    current_player.owned_position.pop(get_oval_obj_key(x_prev, y_prev, current_player), None)
    current_player.owned_position[oval_obj] = (a, b)


def legal_move(x, y, x_prev, y_prev):
    if x_prev == x and y_prev == y:
        return True
    current_index = POINTS.index((x, y))
    previous_index = POINTS.index((x_prev, y_prev))
    print(VALID_MOVES[previous_index])
    if current_index in VALID_MOVES[previous_index]:
        return True
    info['text'] = "Invalid Move  "
    return False


def valid_move_has_empty_cell(tupp):
    for i in tupp:
        x, y = POINTS[i]
        if is_empty(x, y):
            return True
    return False


def is_movable():
    pass


def toggle_turn():
    global current_player
    current_player = players.__next__()


def status_bar():
    if current_player == player_1:
        status['text'] =  player_2.color_notation
    else:
        status['text'] = player_1.color_notation


def exhaust_single_click():
    return len(player_1.owned_position) == 3 and len(player_2.owned_position) == 3


def own_cell(x, y, player):
    if (x, y) in player.owned_position.values():
        return 1


def get_oval_obj_key(x, y, player):
    for key, val in player.owned_position.items():
        if val == (x, y):
            return key


def check_game():
    global current_player
    coordinates = tuple(current_player.owned_position.values())
    if len(coordinates) != 3:
        return 0
    x1, y1 = coordinates[0][0], coordinates[0][1]
    x2, y2 = coordinates[1][0], coordinates[1][1]
    x3, y3 = coordinates[2][0], coordinates[2][1]
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)


def is_empty(x, y):
    if player_1.owned_position or player_2.owned_position:
        if (x, y) in player_1.owned_position.values() or (x, y) in player_2.owned_position.values():
            return 0
    return 1


def all_filled():
    if len(player_1.owned_position) == len(player_2.owned_position) == 3:
        return 1


def bring_oval_in_motion(event, index):
    canvas.coords(index, event.x-30, event.y-30, event.x+30, event.y+30)


def single_click_update(event):
    global ALLOW_SINGLE_CLICK, current_player
    if exhaust_single_click():  # prevent single click if it's exhausted
        ALLOW_SINGLE_CLICK = 0
    if ALLOW_SINGLE_CLICK != 1:
        return
    toggle_turn()
    x, y = event.x, event.y
    (a, b) = get_nearest_node(x, y)
    if a is None or not is_empty(a, b):
        toggle_turn()
        return
    oval_obj = canvas.create_oval(a-30, b-30, a+30, b+30, fill=current_player.color_notation)
    current_player.owned_position[oval_obj] = (a, b)
    status_bar()
    if check_game():
        result()


def double_click_update(event):

    global xprev, yprev, current_player, ALLOW_SINGLE_CLICK, ONE_TIME_CONSTANT
    a, b = get_nearest_node(event.x, event.y)
    if (ALLOW_SINGLE_CLICK != 0) or (invalid_double_click(a, b, xprev)) \
            or (a == xprev and b == yprev):
        if a == xprev and b == yprev:
            info['text'] = "Can't move to same position.  "
        return
    if ONE_TIME_CONSTANT == 1:
        ONE_TIME_CONSTANT -= 1
        toggle_turn()
    if not is_empty(a, b):
        if xprev is None and not own_cell(a, b, current_player):
            info['text'] = "That's not your piece.  "
            return
        elif xprev is not None:
            info['text'] = "INVALID MOVE   "
            return
    info['text'] = ""
    if is_obj_movable(a, b, xprev, current_player, ALLOW_SINGLE_CLICK):
        xprev, yprev = a, b
        current_index = POINTS.index((a, b))
        if not valid_move_has_empty_cell(VALID_MOVES[current_index]):
            info['text'] = "Immovable  "
            xprev, yprev = None, None
            return 0
        canvas.itemconfig(get_oval_obj_key(a, b, current_player), outline="#53f481", width=10)
        index_of_obj = get_oval_obj_key(a, b, current_player)
        canvas.bind("<Motion>", lambda event: bring_oval_in_motion(event, index_of_obj))
    elif check_moving_condition(a, b, xprev, yprev):
        move_a_piece(a, b, xprev, yprev)
        canvas.unbind("<Motion>")
        if check_game():
            result()
        else:
            status_bar()
        toggle_turn()
        xprev = yprev = None


def close():
    root.destroy()


def help_game():
    messagebox.showinfo("Help", "Welcome to the movable tic-tac-toe game. "
                                "The playing rules and win conditions are same "
                                "as that of Tic-Tac-Toe game except the limitation of number of pieces. "
                                "Each player has 3 pieces and after s/he has put all the "
                                "pieces in the board, s/he should drag the pieces. "
                                "Single click to put the piece in the board and double click to drag. "
                                "Double click on the position again to place the dragged piece. "
                                )


draw_grid()
player_1 = Player("Sudarshan", "Blue")
player_2 = Player("Barna", "Red")
players = cycle([player_1, player_2])
info = Label(root, text="", font="Times 12 bold")
info.pack(side=RIGHT)
turn = Label(root, text="  Turn:", font="Times 12 bold", padx=0, pady=5)
turn.pack(side=LEFT, fill=X)
status = Label(root, text=player_1.color_notation , font="Times 12 bold", padx=0, pady=5, bd=6)
status.pack(side=LEFT, fill=X)
canvas.bind('<Double-Button-1>', double_click_update)
canvas.bind('<ButtonPress-1>', single_click_update)

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu =  Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=close)
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_command(label="Help", command=help_game)

root.mainloop()
